# 🚀 D: Drive Research Platform - START HERE

**Welcome to your unified AI research platform!**

---

## ⚡ Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install websocket-client openai python-dotenv fastapi uvicorn
```

### 2. Configure API Key
```bash
# Edit D:\.env and add:
OPENAI_API_KEY=your-key-here
```

### 3. Test Bias Detection
```bash
cd D:\engines\insights\bias
python -m evaluate_bias
```

---

## 📁 What's Where

```
D:\                          ← You are here!
│
├── 🧠 engines/              ← All engines in one place
│   ├── knowledge/          ← Alien Vault, Ollama AI
│   ├── search/             ← Vector search, FAISS
│   ├── insights/           ← ⭐ NEW - Bias detection & research
│   └── scheduling/         ← Automation
│
├── 🌐 api/                  ← API endpoints
├── 📚 bookshelf/            ← Knowledge repository
├── 📊 results/              ← Analysis outputs
└── 📖 docs/                 ← Documentation
```

---

## 🎯 What You Can Do

### **Bias Detection** (Ready Now)
```bash
cd D:\engines\insights\bias
python -m evaluate_bias
```

### **Research Client** (When API running)
```bash
cd D:\engines\insights\client
python -m research_app
```

### **Web Interface** (Turbo Bookshelf)
```bash
cd D:\
python turbo_bookshelf_integration.py web
# Visit: http://localhost:5000
```

### **As Python Module**
```python
import sys
sys.path.insert(0, 'D:\\engines')

from insights.bias import BiasPatternDetector
from insights.client import ResearchApp

# Use it!
detector = BiasPatternDetector()
```

---

## 📚 Documentation

| Read This | For This |
|-----------|----------|
| **MIGRATION_COMPLETE.md** | What was migrated and how |
| **RESEARCH_PLATFORM_ARCHITECTURE.md** | Complete architecture |
| **README_RESEARCH_PLATFORM.md** | Platform overview |
| **CRITICAL_EXECUTION_PLAN.md** | Roadmap & execution plan |

---

## 🎯 Key Features

- ✅ **Bias Detection**: 10 pattern types (5 simple + 5 advanced)
- ✅ **Rate Limiting**: 50 calls/min with exponential backoff
- ✅ **Pattern Analysis**: Research-backed bias patterns
- ✅ **WebSocket Client**: Real-time insights
- ✅ **Turbo Search**: High-performance semantic search
- ✅ **API-First**: All features via REST API

---

## 🔧 Common Tasks

### Test Integration
```bash
python D:\test_integration.py
```

### Run Bias Evaluation
```bash
cd D:\engines\insights\bias
python -m evaluate_bias
```

### Start Web Dashboard
```bash
python D:\turbo_bookshelf_integration.py web
```

### Check System Status
```bash
python D:\turbo_bookshelf_integration.py
```

---

## ❓ Troubleshooting

### "No module named 'websocket'"
```bash
pip install websocket-client
```

### "OPENAI_API_KEY not found"
```bash
# Edit D:\.env
echo "OPENAI_API_KEY=your-key" > D:\.env
```

### "Import Error"
```python
# Add engines to path
import sys
sys.path.insert(0, 'D:\\engines')
```

---

## 🎉 You're Ready!

**Next Command**:
```bash
cd D:\engines\insights\bias
python -m evaluate_bias
```

**Or explore**:
- `D:\RESEARCH_PLATFORM_ARCHITECTURE.md` - Architecture
- `D:\MIGRATION_COMPLETE.md` - What changed
- `D:\docs\insights\` - AI Insights docs

---

**Status**: ✅ Production-ready research platform  
**Location**: D: drive (unified root)  
**Language**: Python only  
**Architecture**: Modular, clean, contextual

🚀 **Happy researching!**
