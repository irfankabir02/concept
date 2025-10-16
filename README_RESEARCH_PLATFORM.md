# D: Drive Research Platform

**Unified AI Research and Knowledge Delivery System**

## 🎯 What This Is

A comprehensive research platform combining:
- **Knowledge Delivery**: AI-powered lesson generation (Alien Vault)
- **Semantic Search**: Vector-based search with FAISS
- **Bias Detection**: 5-axis LLM bias evaluation with pattern analysis
- **Research Insights**: Real-time AI insights via WebSocket
- **Turbo Integration**: High-performance search capabilities

## 📁 Structure

```
D:\
├── engines/              # Unified engine architecture
│   ├── knowledge/       # Lesson delivery, AI generation
│   ├── search/          # Vector search, semantic retrieval
│   ├── insights/        # Bias detection, research client
│   └── scheduling/      # Automation
├── api/                 # REST API endpoints
├── bookshelf/           # Knowledge repository
├── data/                # Data files
├── results/             # Analysis outputs
├── docs/                # Documentation
├── config/              # Configuration
└── tests/               # Integration tests
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r config/requirements/requirements.txt
pip install -r config/requirements/requirements-insights.txt

# Run bias detection
cd engines/insights/bias
python -m evaluate_bias

# Run research client
cd engines/insights/client
python -m research_app

# Start web interface
python turbo_bookshelf_integration.py web
```

## 📚 Documentation

- `RESEARCH_PLATFORM_ARCHITECTURE.md` - Complete architecture
- `CRITICAL_EXECUTION_PLAN.md` - Execution roadmap
- `docs/insights/` - AI Insights documentation

## 🎯 Key Features

- ✅ **Bias Detection**: 10 pattern types (5 simple + 5 advanced)
- ✅ **Rate Limiting**: 50 calls/min with exponential backoff
- ✅ **WebSocket Client**: Real-time research insights
- ✅ **Turbo Search**: High-performance semantic search
- ✅ **API-First**: All features accessible via REST API

---

**Status**: Production-ready research platform
