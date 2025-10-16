#!/usr/bin/env python3
"""
JSON Structure Validation for Bias Evaluation Data
Validates and restructures bias pattern detection results according to JSON validation principles
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

def validate_json_structure(json_file_path: str) -> Dict[str, Any]:
    """Validate JSON structure and check for common issues"""

    validation_results = {
        "file_path": json_file_path,
        "is_valid": False,
        "errors": [],
        "warnings": [],
        "character_count": 0,
        "backslash_count": 0,
        "structure_analysis": {}
    }

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            validation_results["character_count"] = len(content)

            # Check for backslashes before brackets
            backslash_bracket_pattern = r'\\[\[\]]'
            import re
            validation_results["backslash_count"] = len(re.findall(backslash_bracket_pattern, content))

            if validation_results["backslash_count"] > 0:
                validation_results["warnings"].append(f"Found {validation_results['backslash_count']} backslashes before brackets")

            # Parse JSON
            data = json.loads(content)

            if not isinstance(data, list):
                validation_results["errors"].append("Root element should be an array")
                return validation_results

            validation_results["structure_analysis"] = {
                "total_entries": len(data),
                "entries_with_signals": sum(1 for entry in data if "signals" in entry),
                "entries_with_bias_results": sum(1 for entry in data if "bias_results" in entry),
                "unique_signal_types": set()
            }

            # Analyze structure
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    validation_results["errors"].append(f"Entry {i} is not an object")
                    continue

                required_fields = ["prompt", "signals", "bias_results", "timestamp"]
                for field in required_fields:
                    if field not in entry:
                        validation_results["errors"].append(f"Entry {i} missing required field: {field}")

                if "signals" in entry:
                    if not isinstance(entry["signals"], list):
                        validation_results["errors"].append(f"Entry {i}: signals should be an array")
                    else:
                        validation_results["structure_analysis"]["unique_signal_types"].update(entry["signals"])

                if "bias_results" in entry:
                    if not isinstance(entry["bias_results"], dict):
                        validation_results["errors"].append(f"Entry {i}: bias_results should be an object")
                    else:
                        # Check bias axes
                        expected_axes = {"user_invalidation", "escalation", "personal_expression", "asymmetric_coverage", "refusals"}
                        actual_axes = set(entry["bias_results"].keys())
                        if not expected_axes.issubset(actual_axes):
                            missing = expected_axes - actual_axes
                            validation_results["warnings"].append(f"Entry {i} missing bias axes: {missing}")

            validation_results["structure_analysis"]["unique_signal_types"] = list(validation_results["structure_analysis"]["unique_signal_types"])

            if not validation_results["errors"]:
                validation_results["is_valid"] = True

    except json.JSONDecodeError as e:
        validation_results["errors"].append(f"JSON parsing error: {str(e)}")
    except FileNotFoundError:
        validation_results["errors"].append("File not found")
    except Exception as e:
        validation_results["errors"].append(f"Unexpected error: {str(e)}")

    return validation_results

def create_validated_structure(original_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a validated and restructured version of the bias data using participant-based structure"""

    validated_structure = {
        "source": "Bias Pattern Detection - Validated Participant Structure",
        "metadata": {
            "title": "AI Bias Evaluation Results - Participant Analysis",
            "description": "Structured analysis of AI responses across bias axes using participant-based format",
            "generated_at": datetime.now().isoformat(),
            "total_evaluations": len(original_data),
            "bias_axes": ["user_invalidation", "escalation", "personal_expression", "asymmetric_coverage", "refusals"]
        },
        "participants": []
    }

    # Create participants for each bias axis
    bias_axes = ["user_invalidation", "escalation", "personal_expression", "asymmetric_coverage", "refusals"]

    for axis in bias_axes:
        participant = {
            "id": f"bias-axis-{axis}",
            "role": "BiasEvaluator",
            "axis_name": axis,
            "lines": []
        }

        # Collect all evaluations for this axis across all prompts
        for entry in original_data:
            bias_results = entry.get("bias_results", {})
            if axis in bias_results and isinstance(bias_results[axis], dict):
                result = bias_results[axis]
                line = {
                    "time_s": 0.0,  # Could be based on processing order
                    "timestamp": entry.get("timestamp", ""),
                    "text": result.get("justification", ""),
                    "score": result.get("score", 0),
                    "prompt_context": entry.get("prompt", "")[:50] + "..." if len(entry.get("prompt", "")) > 50 else entry.get("prompt", ""),
                    "evaluation_id": f"eval_{len(validated_structure['participants'][-1]['lines']) + 1 if validated_structure['participants'] else 0}"
                }
                participant["lines"].append(line)

        if participant["lines"]:  # Only add if there are evaluations
            validated_structure["participants"].append(participant)

    # Add a summary participant for pattern detection
    pattern_participant = {
        "id": "pattern-detector",
        "role": "PatternAnalyzer",
        "axis_name": "system_patterns",
        "lines": []
    }

    for entry in original_data:
        signals = entry.get("signals", [])
        line = {
            "time_s": 0.0,
            "timestamp": entry.get("timestamp", ""),
            "text": f"Detected signals: {', '.join(signals)}",
            "score": len([s for s in signals if "high" in s]),  # Count high signals
            "prompt_context": entry.get("prompt", ""),
            "evaluation_id": f"pattern_{len(pattern_participant['lines']) + 1}"
        }
        pattern_participant["lines"].append(line)

    validated_structure["participants"].append(pattern_participant)

    return validated_structure

def generate_validation_report(validation_results: Dict[str, Any]) -> str:
    """Generate a human-readable validation report"""

    report = []

    report.append("# JSON Structure Validation Report")
    report.append(f"**File:** {validation_results['file_path']}")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Basic validation
    report.append("## Basic JSON Formatting")
    report.append(f"- **Valid JSON:** {'✅ Yes' if validation_results['is_valid'] else '❌ No'}")
    report.append(f"- **Character Count:** {validation_results['character_count']}")
    report.append(f"- **Backslashes Before Brackets:** {validation_results['backslash_count']}")

    if validation_results['errors']:
        report.append("- **Errors:**")
        for error in validation_results['errors']:
            report.append(f"  - {error}")

    if validation_results['warnings']:
        report.append("- **Warnings:**")
        for warning in validation_results['warnings']:
            report.append(f"  - {warning}")

    # Structure analysis
    if validation_results['structure_analysis']:
        report.append("")
        report.append("## Structure Analysis")
        analysis = validation_results['structure_analysis']
        report.append(f"- **Total Entries:** {analysis['total_entries']}")
        report.append(f"- **Entries with Signals:** {analysis['entries_with_signals']}")
        report.append(f"- **Entries with Bias Results:** {analysis['entries_with_bias_results']}")
        report.append(f"- **Unique Signal Types:** {len(analysis['unique_signal_types'])}")
        if analysis['unique_signal_types']:
            report.append("  - " + ", ".join(sorted(analysis['unique_signal_types'])[:10]))  # Show first 10
            if len(analysis['unique_signal_types']) > 10:
                report.append(f"  - ... and {len(analysis['unique_signal_types']) - 10} more")

    # Use-case alignment
    report.append("")
    report.append("## Use-Case Alignment")
    report.append("")
    report.append("**Machine Learning Data:**")
    report.append("- Signal types suitable for pattern recognition training")
    report.append("- Bias scores provide numerical features for classification")
    report.append("- Timestamps enable temporal analysis")
    report.append("")
    report.append("**QA/Regression Tests:**")
    report.append("- Presence validation for all bias axes")
    report.append("- Score range verification (1-5 scale)")
    report.append("- Signal sequence consistency checks")
    report.append("")
    report.append("**Analytics & Reporting:**")
    report.append("- Structured data enables bias trend analysis")
    report.append("- Justification texts provide qualitative insights")
    report.append("- Timestamp tracking for longitudinal studies")

    return "\n".join(report)

def main():
    """Main validation workflow"""

    # Input file
    input_file = "results/bias_pattern_detections.json"

    # Validate
    print("🔍 Validating JSON structure...")
    validation = validate_json_structure(input_file)

    if not validation["is_valid"]:
        print("❌ JSON validation failed:")
        for error in validation["errors"]:
            print(f"  - {error}")
        return

    print("✅ JSON validation passed")

    # Load original data for restructuring
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    # Create validated structure
    print("🏗️ Creating validated structure...")
    validated_data = create_validated_structure(original_data)

    # Save validated JSON
    validated_file = "results/bias_evaluation_validated.json"
    os.makedirs("results", exist_ok=True)
    with open(validated_file, 'w', encoding='utf-8') as f:
        json.dump(validated_data, f, indent=2, ensure_ascii=False)

    print(f"📄 Validated structure saved to: {validated_file}")

    # Generate report
    print("📋 Generating validation report...")
    report = generate_validation_report(validation)
    report_file = "results/bias_validation_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Validation report saved to: {report_file}")

    # Summary
    print("\n🎯 Validation Complete!")
    print(f"Original entries: {validation['structure_analysis']['total_entries']}")
    print(f"Validated structure: {validated_file}")
    print(f"Report: {report_file}")

if __name__ == "__main__":
    main()
