#!/usr/bin/env python3
"""
VECTOR SYSTEM SETUP
Install Python dependencies for vector embeddings and semantic search
"""

import subprocess
import sys
import os

def install_package(package_name, description=""):
    """Install a Python package using pip"""
    print(f"[VECTOR SETUP] Installing {package_name}...{description}")

    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name, "--quiet"
        ], capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print(f"✓ {package_name} installed successfully")
            return True
        else:
            print(f"✗ Failed to install {package_name}: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ Timeout installing {package_name}")
        return False
    except Exception as e:
        print(f"✗ Error installing {package_name}: {e}")
        return False

def check_package(package_name):
    """Check if a package is installed and working"""
    try:
        if package_name == "faiss-cpu":
            # Special check for faiss
            subprocess.run([
                sys.executable, "-c", "import faiss; print('FAISS version check')"
            ], capture_output=True, check=True, timeout=10)
        else:
            subprocess.run([
                sys.executable, "-c", f"import {package_name.replace('-', '')}"
            ], capture_output=True, check=True, timeout=10)

        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def main():
    print("[VECTOR SETUP] Installing Python dependencies for vector system...")
    print()

    # Required packages for vector embeddings and semantic search
    required_packages = [
        ("sentence-transformers", " (for text embeddings)"),
        ("faiss-cpu", " (for vector similarity search)"),
        ("numpy", " (for numerical computations)"),
        ("pandas", " (for data manipulation)"),
        ("scikit-learn", " (for machine learning utilities)"),
        ("torch", " (PyTorch for deep learning)"),
        ("transformers", " (Hugging Face transformers)"),
        ("requests", " (for API calls)")
    ]

    installed_count = 0
    failed_packages = []

    for package, description in required_packages:
        if install_package(package, description):
            installed_count += 1
        else:
            failed_packages.append(package)

    print()
    print("=" * 50)
    print("INSTALLATION SUMMARY")
    print("=" * 50)

    print(f"Packages attempted: {len(required_packages)}")
    print(f"Successfully installed: {installed_count}")
    print(f"Failed: {len(failed_packages)}")

    if failed_packages:
        print(f"\nFailed packages: {', '.join(failed_packages)}")
        print("\nYou can try installing them manually:")
        for package in failed_packages:
            print(f"  pip install {package}")

    # Verification
    print("\n[VERIFICATION] Testing installations...")
    verification_passed = 0
    verification_total = 0

    test_packages = ["sentence_transformers", "faiss", "numpy", "pandas", "sklearn", "torch", "transformers", "requests"]

    for package in test_packages:
        verification_total += 1
        if check_package(package):
            print(f"✓ {package}")
            verification_passed += 1
        else:
            print(f"✗ {package}")
            failed_packages.append(package)

    print(f"\nVerification: {verification_passed}/{verification_total} packages working")

    if verification_passed >= len(test_packages) * 0.8:  # 80% success rate
        print("\n🎉 VECTOR SYSTEM DEPENDENCIES READY!")
        print("You can now run:")
        print("  bookshelf vector-setup  # Initialize vector index")
        print("  bookshelf vector        # Build embeddings")
        print("  bookshelf search 'query' # Semantic search")
        print("  bookshelf analyze       # Analyze embeddings")
        return True
    else:
        print("\n⚠️  SOME DEPENDENCIES FAILED VERIFICATION")
        print("The system may not work correctly.")
        print("Try reinstalling failed packages or check your Python environment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
