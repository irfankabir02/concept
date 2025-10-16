# 🚀 PowerShell Workflow - D: Drive Research Platform

**Streamlined workflow for PowerShell users**

---

## ✅ **Root Directory Understanding**

**D:\** is now your **unified research platform root** with:
- **engines/** - All Python engines (knowledge, search, insights)
- **api/** - REST API endpoints
- **config/** - Environment and requirements
- **No mixed directories** - Clean separation achieved

---

## 🔧 **What Went Wrong & Fixed**

### **Issue 1: Relative Imports**
**Problem**: `from .rate_limiter` fails in PowerShell
**Root Cause**: Python module execution context
**Fix**: Absolute imports with proper path handling

### **Issue 2: Directory Confusion**
**Problem**: Mixed `engines & logic/` and `engines/` directories
**Root Cause**: Legacy structure vs new structure
**Fix**: Unified `engines/` directory with clear subdirectories

### **Issue 3: PowerShell Path Handling**
**Problem**: Backslash escaping in PowerShell
**Root Cause**: PowerShell vs Unix path differences
**Fix**: PowerShell-specific run scripts and path handling

---

## 🎯 **Streamlined PowerShell Commands**

### **1. Quick Test (No API Key Needed)**
```powershell
# Test bias detection patterns
cd D:\engines\insights\bias
python test_bias_direct.py
```

### **2. Full Bias Evaluation (With API Key)**
```powershell
# Set up environment
cd D:\
$env:PYTHONPATH = "D:\engines"

# Add API key to .env (edit the file first)
notepad D:\.env

# Run bias evaluation
cd D:\engines\insights\bias
python evaluate_bias.py
```

### **3. Research Client**
```powershell
# Start research client
cd D:\engines\insights\client
$env:PYTHONPATH = "D:\engines"
python research_app.py
```

### **4. Web Interface**
```powershell
# Start web interface
cd D:\
python turbo_bookshelf_integration.py web
```

---

## 📁 **PowerShell Directory Structure**

```
D:\                          ← ROOT - Always use this
├── engines/                 ← All Python code here
│   ├── insights/bias/      ← Bias detection
│   ├── insights/client/    ← Research client
│   ├── knowledge/          ← Alien Vault, Ollama
│   └── search/             ← Vector system
├── api/                    ← API endpoints
├── config/                 ← .env file here
└── .env                    ← API key configuration
```

---

## ⚡ **PowerShell Quick Start**

### **Step 1: Test Without API Key**
```powershell
# This works immediately
python D:\engines\insights\bias\test_bias_direct.py
```

### **Step 2: Configure API Key**
```powershell
# Create/edit .env file
notepad D:\.env
# Add: OPENAI_API_KEY=your-key-here
```

### **Step 3: Run Full System**
```powershell
# Set Python path for all commands
$env:PYTHONPATH = "D:\engines"

# Run bias detection
cd D:\engines\insights\bias
python evaluate_bias.py

# Run research client
cd D:\engines\insights\client
python research_app.py
```

---

## 🔍 **PowerShell-Specific Tips**

### **Path Handling**
```powershell
# Always use full paths or set working directory
Set-Location -Path "D:\engines\insights\bias"

# Or use absolute paths
python "D:\engines\insights\bias\test_bias_direct.py"
```

### **Environment Variables**
```powershell
# Temporary for session
$env:PYTHONPATH = "D:\engines"

# Permanent (requires restart)
[System.Environment]::SetEnvironmentVariable("PYTHONPATH", "D:\engines", "User")
```

### **Module Execution**
```powershell
# Don't use -m with relative imports
# Use direct file execution instead
python evaluate_bias.py
```

---

## ✅ **Validation Checklist**

### **Test 1: Structure Check**
```powershell
# Verify structure
ls D:\engines\insights\bias
# Should show: evaluate_bias.py, rate_limiter.py, etc.
```

### **Test 2: Import Check**
```powershell
# Test imports
python -c "import sys; sys.path.insert(0, 'D:\\engines'); from insights.bias import BiasPatternDetector; print('✅ Success')"
```

### **Test 3: Pattern Detection**
```powershell
# Test pattern detection
python D:\engines\insights\bias\test_bias_direct.py
```

---

## 🎯 **One-Command Setup**

```powershell
# Complete setup in one command
Set-Location -Path "D:\"; $env:PYTHONPATH = "D:\engines"; python engines\insights\bias\test_bias_direct.py
```

---

## 🚨 **Common PowerShell Issues & Solutions**

| Issue | Solution |
|-------|----------|
| `ImportError: No module named...` | Set `$env:PYTHONPATH = "D:\engines"` |
| `FileNotFoundError` | Use full paths: `D:\path\to\file.py` |
| `SyntaxError: invalid character` | Use proper PowerShell quotes |
| `ModuleNotFoundError` | Ensure you're in correct directory |

---

## 🎉 **You're Ready!**

**Next Command** (works immediately):
```powershell
python D:\engines\insights\bias\test_bias_direct.py
```

**For full bias evaluation**:
```powershell
# 1. Add API key to D:\.env
# 2. Run:
$env:PYTHONPATH = "D:\engines"
cd D:\engines\insights\bias
python evaluate_bias.py
```

**Platform Status**: ✅ **PowerShell-Ready**
