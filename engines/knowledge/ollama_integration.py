#!/usr/bin/env python3
"""
OLLAMA AI MODEL INTEGRATION
Powers the Bookshelf system with AI-generated content and reasoning
"""

import argparse
import requests
import json
import sys
import time
from typing import Optional, Dict, Any

class OllamaIntegration:
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.timeout = 300  # 5 minutes for generation
        self.models = {
            "embedding": "gemma:latest",
            "general": "cascade",  # Note: user specified "cascade" but this might not exist
            "coder": "qwen3-coder:latest"
        }

    def test_connection(self) -> bool:
        """Test connection to Ollama server"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"[OLLAMA] Connection successful - {len(data.get('models', []))} models available")
                return True
            else:
                print(f"[OLLAMA] HTTP {response.status_code}: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"[OLLAMA] Connection failed: {e}")
            print("Make sure Ollama is running: ollama serve")
            return False

    def list_models(self) -> None:
        """List available models"""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("[OLLAMA] Available Models:")
                for model in data.get('models', []):
                    print(f"  {model['name']} - {model.get('size', 'unknown')} bytes")
            else:
                print(f"[OLLAMA] Failed to list models: HTTP {response.status_code}")
        except Exception as e:
            print(f"[OLLAMA] Error listing models: {e}")

    def generate_response(self, prompt: str, model: str = None, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """Generate response from Ollama model"""
        if model is None:
            model = self.models["general"]

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature
            }
        }

        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"Error: HTTP {response.status_code} - {response.text}"

        except requests.exceptions.Timeout:
            return "Error: Request timed out"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: Unexpected error - {e}"

    def generate_lesson_content(self, category: str, lesson_number: int) -> str:
        """Generate educational content for a lesson"""
        prompts = {
            "BasicReasoning": f"""Generate a concise, educational lesson on basic reasoning and logic concepts. The lesson should be exactly 2-3 sentences long and cover fundamental concepts in:

Lesson Topic Ideas:
- Logic gates and their truth tables
- Boolean algebra principles
- Set theory operations
- Graph theory fundamentals
- Probability theory basics
- Information theory concepts
- Game theory principles
- Decision theory fundamentals
- Causal reasoning concepts
- Abductive reasoning methods

Make it educational and build upon previous knowledge. Focus on one specific concept for lesson {lesson_number}.""",

            "TrainingModules": f"""Generate a concise, educational lesson on computer science and machine learning concepts. The lesson should be exactly 2-3 sentences long and cover:

Lesson Topic Ideas:
- Neural network architectures and training
- Algorithm complexity analysis (Big O notation)
- Database design and normalization
- Computer network protocols and architecture
- Cryptography fundamentals and applications
- Data structures and their applications
- Machine learning supervised vs unsupervised
- Computer vision techniques
- Natural language processing methods
- Reinforcement learning algorithms

Make it educational and build upon previous knowledge. Focus on one specific concept for lesson {lesson_number}.""",

            "TestingProtocols": f"""Generate a concise, educational lesson on software testing and quality assurance. The lesson should be exactly 2-3 sentences long and cover:

Lesson Topic Ideas:
- Unit testing principles and practices
- Integration testing strategies
- System testing methodologies
- Security testing and penetration testing
- Performance testing and benchmarking
- Regression testing techniques
- User acceptance testing processes
- Chaos engineering principles
- A/B testing statistical methods
- Continuous integration testing

Make it educational and build upon previous knowledge. Focus on one specific concept for lesson {lesson_number}.""",

            "CrazyDiamonds": f"""Generate a concise, educational lesson on creative thinking and innovation concepts. The lesson should be exactly 2-3 sentences long and cover:

Lesson Topic Ideas:
- Creative thinking techniques (divergent vs convergent)
- Innovation methodologies (Design Thinking, TRIZ, SCAMPER)
- Imagination development and mental imagery
- Artistic expression and creative processes
- Musical creativity and composition techniques
- Literary innovation and narrative structures
- Entrepreneurial vision and opportunity recognition
- Scientific discovery processes and hypothesis generation
- Technological invention and prototyping
- Philosophical inquiry and thought experiments

Make it educational and build upon previous knowledge. Focus on one specific concept for lesson {lesson_number}."""
        }

        prompt = prompts.get(category, f"Generate educational content about {category}")
        print(f"[OLLAMA] Generating {category} lesson #{lesson_number}...")

        content = self.generate_response(prompt, max_tokens=300, temperature=0.3)

        # Clean up response
        if content.startswith("Error:"):
            print(f"[OLLAMA] Generation failed: {content}")
            return f"Advanced concepts in {category} - Lesson {lesson_number}"

        # Remove any unwanted formatting
        content = content.strip()
        if content.startswith("Lesson:") or content.startswith("**"):
            content = content.split(":", 1)[-1].strip()
            content = content.lstrip("*").strip()

        return content

    def generate_reality_check(self, category: str, content: str) -> str:
        """Generate a reality check question based on lesson content"""
        prompt = f"""Based on this lesson content, generate a thoughtful reality-check question that tests understanding:

Lesson Content: {content}

Generate a single, specific question that requires the learner to apply or recall the key concepts from this lesson. The question should be challenging but answerable based on the content provided.

Format your response with just the question - no additional formatting or explanations."""

        print("[OLLAMA] Generating reality check question...")

        question = self.generate_response(prompt, max_tokens=150, temperature=0.2)

        if question.startswith("Error:"):
            print(f"[OLLAMA] Reality check generation failed: {question}")
            # Fallback questions
            fallbacks = {
                "BasicReasoning": "What fundamental concept was explained in this logic lesson?",
                "TrainingModules": "What key principle was covered in this computer science lesson?",
                "TestingProtocols": "What testing methodology was discussed in this lesson?",
                "CrazyDiamonds": "What creative thinking technique was explored in this lesson?"
            }
            return fallbacks.get(category, "What key concept was covered in this lesson?")

        # Clean up response
        question = question.strip()
        if question.startswith("Question:") or question.startswith("Q:"):
            question = question.split(":", 1)[-1].strip()

        return question

    def generate_embeddings(self, text: str) -> str:
        """Generate embeddings for text (placeholder for future vector search)"""
        # This is a simplified placeholder
        # In a real implementation, this would call the embedding API
        import hashlib
        hash_obj = hashlib.sha256(text.encode('utf-8'))
        return hash_obj.hexdigest()[:32]


def main():
    parser = argparse.ArgumentParser(description="Ollama AI Model Integration")
    parser.add_argument("-TestConnection", action="store_true", help="Test Ollama connection")
    parser.add_argument("-ListModels", action="store_true", help="List available models")
    parser.add_argument("-GenerateLesson", action="store_true", help="Generate lesson content")
    parser.add_argument("-GenerateRealityCheck", action="store_true", help="Generate reality check")
    parser.add_argument("-Category", type=str, help="Lesson category")
    parser.add_argument("-LessonNumber", type=int, help="Lesson number")
    parser.add_argument("-Content", type=str, help="Lesson content for reality check")
    parser.add_argument("-Prompt", type=str, help="Custom prompt for generation")
    parser.add_argument("-Model", type=str, default="gemma:latest", help="Model to use")
    parser.add_argument("-Host", type=str, default="http://localhost:11434", help="Ollama host")

    args = parser.parse_args()

    try:
        ollama = OllamaIntegration(host=args.Host)

        if args.TestConnection:
            success = ollama.test_connection()
            sys.exit(0 if success else 1)

        elif args.ListModels:
            ollama.list_models()
            sys.exit(0)

        elif args.GenerateLesson:
            if not args.Category or not args.LessonNumber:
                print("ERROR: Must specify -Category and -LessonNumber for lesson generation")
                sys.exit(1)

            content = ollama.generate_lesson_content(args.Category, args.LessonNumber)
            print(content)
            sys.exit(0)

        elif args.GenerateRealityCheck:
            if not args.Category or not args.Content:
                print("ERROR: Must specify -Category and -Content for reality check generation")
                sys.exit(1)

            question = ollama.generate_reality_check(args.Category, args.Content)
            print(question)
            sys.exit(0)

        elif args.Prompt:
            response = ollama.generate_response(args.Prompt, model=args.Model)
            print("AI Response:")
            print(response)
            sys.exit(0)

        else:
            print("=== OLLAMA AI MODEL INTEGRATION ===")
            print()
            print("Configured Models:")
            print(f"  General Purpose: {ollama.models['general']}")
            print(f"  Embedding Model: {ollama.models['embedding']}")
            print(f"  Coding Model: {ollama.models['coder']}")
            print()
            print("Usage:")
            print("  python ollama_integration.py -TestConnection")
            print("  python ollama_integration.py -ListModels")
            print("  python ollama_integration.py -GenerateLesson -Category BasicReasoning -LessonNumber 1")
            print("  python ollama_integration.py -Prompt 'Hello AI'")
            print()
            print(f"Ollama Host: {ollama.host}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
