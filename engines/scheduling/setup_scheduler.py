#!/usr/bin/env python3
"""
ALIEN VAULT SCHEDULER SETUP
Creates scheduled task for daily 12AM lesson delivery
"""

import argparse
import subprocess
import sys
import os

class SchedulerSetup:
    def __init__(self):
        self.task_name = "AlienVault-DailyLesson"
        self.script_path = r"D:\engines & logic\alien_vault_delivery.py"

    def validate_script(self) -> bool:
        """Check if the delivery script exists"""
        if not os.path.exists(self.script_path):
            print(f"ERROR: Script not found: {self.script_path}")
            return False
        return True

    def remove_existing_task(self) -> None:
        """Remove existing scheduled task if it exists"""
        try:
            result = subprocess.run(
                ["schtasks", "/delete", "/tn", self.task_name, "/f"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"[REMOVE] Deleted existing task: {self.task_name}")
        except subprocess.TimeoutExpired:
            print("[WARNING] Task deletion timed out")
        except Exception as e:
            # Task might not exist, which is fine
            pass

    def create_scheduled_task(self) -> bool:
        """Create the daily scheduled task"""
        # Command to run: python script_path
        command = f'python "{self.script_path}"'

        try:
            # Create scheduled task using schtasks
            result = subprocess.run([
                "schtasks", "/create",
                "/tn", self.task_name,
                "/tr", command,
                "/sc", "daily",
                "/st", "00:00",
                "/rl", "highest",
                "/f"  # Force overwrite
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print("SUCCESS: Scheduled task created!")
                print("Daily delivery at 12:00 AM (midnight)")
                print("Task will run with highest privileges")
                return True
            else:
                print(f"ERROR: Failed to create task: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            print("ERROR: Task creation timed out")
            return False
        except Exception as e:
            print(f"ERROR: Task creation failed: {e}")
            return False

    def test_task(self) -> None:
        """Test the delivery system"""
        try:
            print("[TEST] Testing Alien Vault Delivery System...")
            result = subprocess.run([
                sys.executable, self.script_path, "--progress"
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print("SUCCESS: System test completed!")
                print("Output:")
                print(result.stdout)
            else:
                print(f"ERROR: System test failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            print("ERROR: Test timed out")
        except Exception as e:
            print(f"ERROR: Test failed: {e}")

    def show_status(self) -> None:
        """Show current scheduler status"""
        print("[STATUS] Alien Vault Scheduler Status")

        try:
            result = subprocess.run([
                "schtasks", "/query", "/tn", self.task_name, "/fo", "list", "/v"
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0 and "AlienVault-DailyLesson" in result.stdout:
                print("ACTIVE: Task Status - Ready")

                # Extract next run time
                for line in result.stdout.split('\n'):
                    if "Next Run Time:" in line:
                        print(f"Next Run: {line.split(':', 1)[1].strip()}")
                    elif "Last Run Time:" in line:
                        print(f"Last Run: {line.split(':', 1)[1].strip()}")
                    elif "Task To Run:" in line:
                        print(f"Command: {line.split(':', 1)[1].strip()}")

                # Show progress
                print()
                print("[Bookshelf] Progress:")
                subprocess.run([sys.executable, self.script_path, "--progress"])
            else:
                print("NOT FOUND: Scheduled task not found")
                print("Run with -Install to create the task")

        except subprocess.TimeoutExpired:
            print("ERROR: Status check timed out")
        except Exception as e:
            print(f"ERROR: Status check failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Alien Vault Scheduler Setup")
    parser.add_argument("-Install", action="store_true", help="Install scheduled task")
    parser.add_argument("-Remove", action="store_true", help="Remove scheduled task")
    parser.add_argument("-Test", action="store_true", help="Test the delivery system")

    args = parser.parse_args()

    try:
        scheduler = SchedulerSetup()

        if args.Install:
            if not scheduler.validate_script():
                sys.exit(1)

            scheduler.remove_existing_task()
            if scheduler.create_scheduled_task():
                print("\n[SUCCESS] Daily lesson scheduler is now active!")
                print("Lessons will be delivered automatically at midnight.")
            else:
                sys.exit(1)

        elif args.Remove:
            scheduler.remove_existing_task()
            print("SUCCESS: Scheduled task removed!")

        elif args.Test:
            scheduler.test_task()

        else:
            scheduler.show_status()

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
