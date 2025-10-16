# Plan-Execution Gap Analysis & Restructuring

**Date**: October 16, 2025, 5:23am  
**Status**: Restructuring for simplified workflow

---

## 🎯 Original Plan vs Current State

### ✅ What Was Completed

**Sprint 1 (Complete)**:
- ✅ Error handling (`bias/evaluate_bias.py`)
- ✅ Rate limiting (`bias/rate_limiter.py`)
- ✅ Bias patterns (`bias/bias_pattern_detector.py`, `bias/advanced_bias_patterns.py`)

**Research Lens Scaffold (Complete but needs restructuring)**:
- ✅ FastAPI backend designed
- ✅ Python client created
- ✅ Documentation written

---

## 🚨 Identified Gaps

### 1. **Path Complexity** ❌
**Problem**: Multiple nested directories confuse workflow
```
❌ research-lens/backend/client/websocket_client.py
❌ research-lens/backend/api/main.py
❌ research-lens/frontend/src/... (unused, switched to Python)
```

**Solution**: Flatten to root-level structure
```
✅ client/websocket_client.py
✅ api/main.py
✅ bias/... (existing)
```

### 2. **Language Split** ❌
**Problem**: React/TypeScript planned but user prefers Python-only
- Frontend planned in React (not needed)
- User translated to Python
- Mixed documentation (React + Python)

**Solution**: Python-only repository
- Remove React references
- Single language = holistic codebase
- Clearer dependencies

### 3. **Incomplete Backend** ❌
**Problem**: FastAPI stubs not implemented
- `rag_engine.py` - placeholder only
- `physics_engine.py` - placeholder only
- `space_engine.py` - placeholder only
- `redis_cache.py` - not connected

**Solution**: Implement or remove unused stubs

### 4. **Scattered Documentation** ❌
**Problem**: Too many README files
- `README.md` (root)
- `research-lens/README.md`
- `research-lens/SETUP_GUIDE.md`
- `research-lens/PYTHON_CLIENT_GUIDE.md`
- etc.

**Solution**: One main README at root, organized sections

### 5. **No Integration** ❌
**Problem**: research-lens not integrated with bias modules
- Separate project structure
- Not using Sprint 1 work effectively
- Duplication potential

**Solution**: Integrate into unified codebase

---

## 🔧 Restructuring Plan

### New Directory Structure (Python-Only)

```
ai-insights-experiments/           # ROOT - Work here
├── .env                           # Config
├── .gitignore
├── requirements.txt               # ← Unified dependencies
├── README.md                      # ← Single source of truth
│
├── bias/                          # ← Sprint 1 (keep as-is)
│   ├── evaluate_bias.py
│   ├── rate_limiter.py
│   ├── bias_pattern_detector.py
│   └── advanced_bias_patterns.py
│
├── api/                           # ← Research Lens API (moved from research-lens/backend/api)
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── routes.py
│   └── middleware.py
│
├── engines/                       # ← Analysis engines (moved from research-lens/backend/engines)
│   ├── __init__.py
│   ├── rag_engine.py              # SELF-RAG (implement)
│   ├── bias_engine.py             # Uses bias/ modules
│   ├── physics_engine.py          # SymPy/NumPy (implement)
│   └── space_engine.py            # NASA API (implement)
│
├── client/                        # ← Python console client (moved)
│   ├── __init__.py
│   ├── websocket_client.py
│   ├── research_app.py
│   └── formatters.py
│
├── core/                          # ← Core utilities (moved)
│   ├── __init__.py
│   ├── intent_classifier.py
│   ├── vector_scorer.py
│   └── config.py
│
├── db/                            # ← Database (moved)
│   ├── __init__.py
│   ├── redis_cache.py
│   └── postgres.py
│
├── data/                          # ← Data files
│   └── prompts.json
│
├── results/                       # ← Output files
│   └── bias_evaluation.json
│
├── tests/                         # ← All tests here
│   ├── test_bias.py
│   ├── test_api.py
│   ├── test_engines.py
│   └── test_client.py
│
├── scripts/                       # ← Utility scripts
│   ├── run_server.py
│   ├── test_all.py
│   └── setup_db.py
│
└── docs/                          # ← All documentation
    ├── API.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

---

## 🎯 Immediate Actions

### Phase 1: Restructure (Now)
- [ ] Move `/research-lens/backend/api/*` → `/api/`
- [ ] Move `/research-lens/backend/engines/*` → `/engines/`
- [ ] Move `/research-lens/backend/client/*` → `/client/`
- [ ] Move `/research-lens/backend/core/*` → `/core/`
- [ ] Move `/research-lens/backend/db/*` → `/db/`
- [ ] Consolidate `requirements.txt` at root
- [ ] Update all import paths
- [ ] Delete `/research-lens/` directory

### Phase 2: Consolidate Documentation
- [ ] Merge all READMEs into single root README
- [ ] Create `/docs/` folder for detailed guides
- [ ] Remove redundant documentation

### Phase 3: Implement Missing Pieces
- [ ] Implement `rag_engine.py` (SELF-RAG)
- [ ] Implement `physics_engine.py` (SymPy)
- [ ] Implement `space_engine.py` (NASA API)
- [ ] Connect `redis_cache.py`
- [ ] Integrate with Sprint 1 bias modules

### Phase 4: Testing
- [ ] Move all tests to `/tests/`
- [ ] Create `test_all.py` runner
- [ ] Validate end-to-end workflow

---

## 📊 Gap Summary

| Gap | Impact | Priority | Status |
|-----|--------|----------|--------|
| Path complexity | High | P0 | Fixing now |
| Mixed languages | High | P0 | Removing React |
| Incomplete engines | Medium | P1 | TODO |
| Scattered docs | Medium | P1 | Consolidating |
| No integration | High | P0 | Fixing now |

---

## ✅ Simplified Workflow (After Restructure)

```bash
# Work at root
cd ai-insights-experiments

# Install
pip install -r requirements.txt

# Run API
python -m api.main

# Run client
python -m client.research_app

# Run bias evaluation
python -m bias.evaluate_bias

# Run all tests
python -m tests.test_all
```

**All Python. All at root. One language. Holistic and functional.**

---

## 🎯 Next Step

Execute Phase 1: Restructure files to root-level simplified structure.
