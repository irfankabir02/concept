#!/usr/bin/env python3
"""
SEMANTIC VECTOR SEARCH SYSTEM
Analyzes trajectory and future directions using vector embeddings
"""

import os
import json
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Check if vector dependencies are available
try:
    import sentence_transformers
    from sentence_transformers import SentenceTransformer
    import faiss
    import torch
    VECTOR_DEPS_AVAILABLE = True
except ImportError:
    VECTOR_DEPS_AVAILABLE = False

class SemanticTrajectoryAnalyzer:
    def __init__(self):
        self.root_path = Path("D:\\")
        self.model = None
        self.index = None
        self.documents = []
        self.metadata = []

        if not VECTOR_DEPS_AVAILABLE:
            print("⚠️  Vector dependencies not available. Run 'bookshelf vector-setup' first.")
            return

        # Initialize the model
        try:
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("✅ Semantic model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load semantic model: {e}")
            self.model = None

    def load_documents(self):
        """Load all relevant documents for analysis"""
        document_paths = [
            # Core system documentation
            "engines & logic/README.md",
            "bookshelf/WELCOME.md",
            "docs/README_HARMONYHUB.md",
            "docs/HARMONYHUB_INTEGRATION_COMPLETE.md",
            "docs/HARMONYHUB_WORKFLOW_GUIDE.md",
            "docs/principles.md",

            # Automation framework
            "automation-framework/AUTOMATION_ANALYSIS.md",

            # Archives and lessons
            "Archives/MANIFEST.md",

            # Research and reports
            "reprots/TRANSFORMERS_THE_BASICS_on_MINI-CONS_20251009_190958.txt",

            # Configuration files
            "project_config.json",
            "automation-framework/automation_config.json",
        ]

        for doc_path in document_paths:
            full_path = self.root_path / doc_path
            if full_path.exists():
                try:
                    if full_path.suffix == '.json':
                        with open(full_path, 'r') as f:
                            content = json.dumps(json.load(f), indent=2)
                    else:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                    self.documents.append(content)
                    self.metadata.append({
                        'path': str(full_path),
                        'filename': full_path.name,
                        'type': full_path.suffix,
                        'size': len(content)
                    })
                    print(f"📄 Loaded: {doc_path} ({len(content)} chars)")

                except Exception as e:
                    print(f"❌ Failed to load {doc_path}: {e}")

        print(f"\n📚 Loaded {len(self.documents)} documents for analysis")

    def build_index(self):
        """Build FAISS vector index"""
        if not self.model or not self.documents:
            print("❌ Cannot build index: model or documents not available")
            return

        print("🔨 Building semantic index...")

        try:
            # Generate embeddings
            embeddings = self.model.encode(self.documents, show_progress_bar=True)
            embeddings = np.array(embeddings, dtype=np.float32)

            # Normalize for cosine similarity
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1
            embeddings = embeddings / norms

            # Create FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine
            self.index.add(embeddings)

            print(f"✅ Index built: {len(self.documents)} documents, {dimension}D vectors")

        except Exception as e:
            print(f"❌ Failed to build index: {e}")

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform semantic search"""
        if not self.model or not self.index:
            print("❌ Search unavailable: model or index not ready")
            return []

        try:
            # Encode query
            query_embedding = self.model.encode([query])[0]
            query_embedding = np.array([query_embedding], dtype=np.float32)

            # Normalize
            norm = np.linalg.norm(query_embedding)
            if norm > 0:
                query_embedding = query_embedding / norm

            # Search
            scores, indices = self.index.search(query_embedding, top_k)

            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'score': float(score),
                        'document': self.documents[idx][:500] + "..." if len(self.documents[idx]) > 500 else self.documents[idx],
                        'metadata': self.metadata[idx],
                        'relevance': self._interpret_score(score)
                    })

            return results

        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []

    def _interpret_score(self, score: float) -> str:
        """Interpret semantic similarity score"""
        if score > 0.8:
            return "Very High"
        elif score > 0.6:
            return "High"
        elif score > 0.4:
            return "Medium"
        elif score > 0.2:
            return "Low"
        else:
            return "Very Low"

    def analyze_trajectory(self) -> Dict[str, Any]:
        """Analyze the overall trajectory and future directions"""

        # Key trajectory queries
        trajectory_queries = [
            "What is the main purpose or vision of this system?",
            "What technologies and frameworks are being used?",
            "What are the current capabilities and features?",
            "What future directions or goals are mentioned?",
            "What challenges or limitations are discussed?",
            "What automation or AI capabilities exist?",
            "What learning or knowledge systems are in place?",
            "What integration points or APIs are available?",
            "What security or reliability measures are implemented?",
            "What scalability or performance considerations exist?"
        ]

        trajectory_analysis = {}

        print("🔍 Analyzing trajectory across all documents...")

        for query in trajectory_queries:
            print(f"  Query: {query}")
            results = self.semantic_search(query, top_k=3)
            trajectory_analysis[query] = results

        return trajectory_analysis

    def identify_future_vectors(self) -> List[Dict[str, Any]]:
        """Identify potential future development vectors"""

        future_queries = [
            "expansion opportunities",
            "new features to add",
            "integration possibilities",
            "scalability improvements",
            "performance optimizations",
            "new technologies to adopt",
            "market opportunities",
            "research directions",
            "collaboration potential",
            "monetization strategies"
        ]

        vectors = []

        print("🚀 Identifying future development vectors...")

        for query in future_queries:
            print(f"  Exploring: {query}")
            results = self.semantic_search(query, top_k=2)

            if results and results[0]['score'] > 0.3:  # Only include relevant results
                vectors.append({
                    'direction': query,
                    'relevance_score': results[0]['score'],
                    'key_insights': [r['document'][:200] for r in results[:2]],
                    'source_documents': [r['metadata']['filename'] for r in results[:2]]
                })

        # Sort by relevance
        vectors.sort(key=lambda x: x['relevance_score'], reverse=True)

        return vectors

    def generate_trajectory_report(self) -> str:
        """Generate comprehensive trajectory analysis report"""

        if not VECTOR_DEPS_AVAILABLE:
            return "❌ Vector dependencies not available. Run 'bookshelf vector-setup' first."

        self.load_documents()

        if not self.documents:
            return "❌ No documents found to analyze."

        self.build_index()

        if not self.index:
            return "❌ Failed to build semantic index."

        # Analyze trajectory
        trajectory = self.analyze_trajectory()
        vectors = self.identify_future_vectors()

        # Generate report
        report = []
        report.append("# 🚀 SEMANTIC TRAJECTORY ANALYSIS")
        report.append(f"**Analysis Date:** {self._get_timestamp()}")
        report.append(f"**Documents Analyzed:** {len(self.documents)}")
        report.append(f"**Total Content Size:** {sum(len(d) for d in self.documents)} characters")
        report.append("")

        # Current State Summary
        report.append("## 📊 CURRENT SYSTEM STATE")
        report.append("")
        report.append("### Core Purpose & Vision")
        if "What is the main purpose or vision of this system?" in trajectory:
            results = trajectory["What is the main purpose or vision of this system?"]
            for result in results[:2]:
                report.append(f"- **{result['relevance']} relevance**: {result['document'][:150]}...")

        report.append("")
        report.append("### Technology Stack")
        if "What technologies and frameworks are being used?" in trajectory:
            results = trajectory["What technologies and frameworks are being used?"]
            tech_mentions = []
            for result in results:
                doc = result['document'].lower()
                if 'python' in doc: tech_mentions.append('Python')
                if 'ollama' in doc: tech_mentions.append('Ollama AI')
                if 'vector' in doc: tech_mentions.append('Vector Search')
                if 'automation' in doc: tech_mentions.append('Automation')
                if 'harmonyhub' in doc: tech_mentions.append('HarmonyHub')
            tech_mentions = list(set(tech_mentions))
            for tech in tech_mentions:
                report.append(f"- {tech}")

        report.append("")
        report.append("### Key Capabilities")
        capabilities = []
        for query, results in trajectory.items():
            if 'capabilities' in query.lower() or 'features' in query.lower():
                for result in results[:1]:
                    capabilities.append(f"- {result['document'][:100]}...")

        if capabilities:
            report.extend(capabilities[:3])
        else:
            report.append("- AI-powered knowledge delivery system")
            report.append("- Semantic search and vector embeddings")
            report.append("- Automated learning progression")

        # Future Directions
        report.append("")
        report.append("## 🎯 FUTURE DEVELOPMENT VECTORS")
        report.append("")

        if vectors:
            for i, vector in enumerate(vectors[:8], 1):  # Top 8 directions
                report.append(f"### {i}. {vector['direction'].title()}")
                report.append(f"**Relevance:** {vector['relevance_score']:.2f}")
                report.append(f"**Key Insight:** {vector['key_insights'][0]}")
                report.append(f"**Source:** {vector['source_documents'][0]}")
                report.append("")

        # Recommendations
        report.append("## 💡 RECOMMENDED NEXT STEPS")
        report.append("")
        report.append("### High-Impact Opportunities:")
        report.append("1. **Expand AI Integration** - Leverage existing Ollama setup for more advanced features")
        report.append("2. **Enhance Automation** - Build on the automation framework for workflow optimization")
        report.append("3. **Scale Knowledge System** - Expand the Bookshelf with more specialized domains")
        report.append("4. **API Development** - Create external APIs for system integration")
        report.append("5. **User Experience** - Develop web interfaces for broader accessibility")
        report.append("")

        report.append("### Implementation Priority:")
        report.append("- **Immediate**: Vector search optimization and content expansion")
        report.append("- **Short-term**: Web interface development and API creation")
        report.append("- **Long-term**: Multi-user support and enterprise features")
        report.append("")

        return "\n".join(report)

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    parser = argparse.ArgumentParser(description="Semantic Trajectory Analyzer")
    parser.add_argument("-q", "--query", help="Specific semantic search query")
    parser.add_argument("-k", "--top_k", type=int, default=5, help="Number of results to return")
    parser.add_argument("-o", "--output", help="Output file for trajectory report")
    parser.add_argument("-t", "--trajectory", action="store_true", help="Generate full trajectory analysis")

    args = parser.parse_args()

    analyzer = SemanticTrajectoryAnalyzer()

    if not VECTOR_DEPS_AVAILABLE:
        print("❌ Vector dependencies not available.")
        print("Run 'bookshelf vector-setup' to install required packages.")
        sys.exit(1)

    if args.trajectory or not args.query:
        # Generate full trajectory report
        print("🚀 Generating comprehensive trajectory analysis...")
        report = analyzer.generate_trajectory_report()

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.output}")
        else:
            print(report)

    elif args.query:
        # Single query search
        analyzer.load_documents()
        analyzer.build_index()

        print(f"🔍 Searching for: '{args.query}'")
        results = analyzer.semantic_search(args.query, args.top_k)

        if results:
            print(f"\n📋 Top {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['relevance']} Relevance ({result['score']:.3f})")
                print(f"   Source: {result['metadata']['filename']}")
                print(f"   Content: {result['document'][:200]}...")
        else:
            print("❌ No relevant results found.")

if __name__ == "__main__":
    main()
