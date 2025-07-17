# 🚀 Adobe India Hackathon 2025 - Connecting the Dots

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![Platform](https://img.shields.io/badge/Platform-linux%2Famd64-green.svg)](https://docs.docker.com/desktop/multi-arch/)

> **🏆 OPTIMIZED SOLUTION - All Constraints Satisfied**  
> Docker Image: **200MB** (≤1GB requirement ✅)  
> Performance: **Round 1A: 2.8s** | **Round 1B: 3.8s** ✅

## 📋 Overview

Intelligent, offline-compatible document analysis system supporting:

- **🔍 Round 1A**: Extract structured PDF outlines (Title, H1-H3 headings + page numbers)
- **🧠 Round 1B**: Persona-driven document intelligence with relevance ranking

### ✨ Key Features

- **🎯 Unified Solution**: Single Docker container auto-detects Round 1A vs 1B
- **⚡ High Performance**: Exceeds speed requirements (10s/60s limits)
- **🔒 Offline First**: No internet access required, fully containerized
- **📊 Smart Detection**: Automatic persona classification (Travel, HR, Cooking)
- **🏗️ Modular Design**: Clean separation of concerns with src/ architecture

## 🚀 Quick Start

### Build & Run
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-analyzer .

# Run Round 1A (PDF outline extraction)
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-analyzer

# Run Round 1B (with persona intelligence)
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/persona:/app/persona \
  --network none \
  pdf-analyzer
```

### Test Scripts
```bash
# Windows
.\scripts\build_and_test.ps1

# Linux/macOS  
./scripts/build_and_test.sh
```

## 📁 Project Structure

```
📦 Adobe Hackathon Solution
├── 🐳 Dockerfile              # Optimized container (200MB)
├── 🎯 main.py                 # Unified entry point with auto-detection
├── 📂 src/
│   ├── 📄 process_pdfs.py     # Round 1A: PDF outline extraction
│   └── 🧠 persona_intelligence.py # Round 1B: Persona-driven analysis
├── 📂 scripts/               # Build and test automation
├── 📂 tests/                 # Test suite
├── 📂 docs/                  # Documentation
└── 📂 Dataset/               # Sample data for testing
```

## 🧪 Performance Metrics

| **Constraint** | **Requirement** | **Actual** | **Status** |
|----------------|-----------------|------------|------------|
| Round 1A Speed | ≤10s per 50-page PDF | 2.8s for 5 PDFs | ✅ **PASS** |
| Round 1B Speed | ≤60s for 3-5 PDFs | 3.8s for 12 PDFs | ✅ **PASS** |
| Round 1A Model | ≤200MB | No models | ✅ **PASS** |
| Round 1B Model | ≤1GB | 200MB total | ✅ **PASS** |
| Platform | linux/amd64 | ✅ | ✅ **PASS** |
| Network | Offline only | ✅ | ✅ **PASS** |

## 🎯 Round Details

### Round 1A: PDF Outline Extraction
- **Input**: PDFs in `/app/input`
- **Output**: JSON files with title and heading hierarchy
- **Technology**: PyPDF2 + PyMuPDF for robust text extraction
- **Performance**: <10 seconds per document

### Round 1B: Persona Intelligence  
- **Input**: PDFs + `persona/persona.json`
- **Output**: Ranked relevant sections with importance scores
- **Intelligence**: Auto-detects Travel Planner, HR Professional, or Home Cook personas
- **Performance**: <60 seconds for document collections

## 🔧 Technical Architecture

### Smart Detection Logic
```python
def detect_input_type():
    """Auto-detect Round 1A vs 1B based on input structure"""
    has_persona = os.path.exists('/app/persona')
    has_persona_file = os.path.exists('/app/persona/persona.json')
    return "Round1B" if has_persona else "Round1A"
```

### Persona Classification
- **Travel Planner**: Detects tourism, destinations, activities
- **HR Professional**: Identifies skills, recruitment, training content  
- **Home Cook**: Recognizes recipes, ingredients, cooking techniques

## 📊 Output Schema

### Round 1A Example
```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Main Section", "page": 1 },
    { "level": "H2", "text": "Subsection", "page": 2 }
  ]
}
```

### Round 1B Example
```json
{
  "metadata": {
    "persona": "Travel Planner",
    "documents": ["doc1.pdf", "doc2.pdf"],
    "timestamp": "2025-07-18T10:30:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 3,
      "section_title": "Travel Destinations",
      "importance_rank": 1
    }
  ]
}
```

## 🏗️ Development

### Prerequisites
- Docker with linux/amd64 support
- Python 3.10+ (for local development)

### Dependencies
```
PyPDF2==3.0.1      # PDF text extraction
PyMuPDF==1.26.3    # Advanced PDF processing
```

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run local tests
python -m pytest tests/

# Manual testing
python main.py
```

*For detailed technical documentation, see [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)*

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

**🏆 Built for Adobe India Hackathon 2025 - "Connecting the Dots"**

*Optimized solution meeting all performance and size constraints* ✨
