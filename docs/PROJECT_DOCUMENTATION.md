# Adobe India Hackathon Round 1A - Documentation

## Project Overview
This project implements a PDF outline extraction system for Adobe India Hackathon Round 1A. The system extracts titles and headings from PDF documents and outputs them in a structured JSON format.

## Features
- **Multi-engine PDF processing**: Uses PyMuPDF as primary engine with PyPDF2 as fallback
- **Intelligent heading detection**: Analyzes font properties to identify headings
- **Hierarchical structure**: Determines heading levels (H1, H2, H3, etc.)
- **Robust error handling**: Handles various PDF formats and edge cases
- **Performance optimized**: Processes files in <0.2s average time
- **Docker containerized**: Ready for production deployment

## Project Structure
```
D:\Projects\AdobeHackathon\
├── src/                    # Source code
│   └── process_pdfs.py    # Main PDF processing engine
├── scripts/               # Utility scripts
│   ├── run_solution.py    # Local solution runner
│   ├── build_and_test.ps1 # PowerShell build script
│   ├── build_and_test.sh  # Unix build script
│   └── quick_test.ps1     # Quick test runner
├── tests/                 # Test files
│   ├── test_local.py      # Local functionality tests
│   └── test_performance.py # Performance validation
├── docs/                  # Documentation
├── input/                 # Input PDF files
├── output/                # Output JSON files
├── Dataset/               # Challenge data
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project README
```

## Quick Start

### 1. Quick Local Test
```powershell
# Windows PowerShell
.\scripts\quick_test.ps1
```

### 2. Full Docker Build and Test
```powershell
# Windows PowerShell
.\scripts\build_and_test.ps1
```

```bash
# Unix/Linux
./scripts/build_and_test.sh
```

### 3. Manual Docker Run
```bash
# Build image
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

# Run container
docker run --rm \
    -v "$(pwd)/input:/app/input" \
    -v "$(pwd)/output:/app/output" \
    --network none \
    pdf-outline-extractor:latest
```

## Dependencies
- Python 3.10+
- PyMuPDF 1.23.8
- PyPDF2 3.0.1

## Output Format
The system generates JSON files with the following structure:
```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Heading",
      "page": 0
    },
    {
      "level": "H2", 
      "text": "Sub Heading",
      "page": 1
    }
  ]
}
```

## Performance
- Average processing time: <0.2s per file (0.03s average across 5 test files)
- Total processing time: 0.16s for all 5 test files
- Memory usage: Optimized for large documents
- Error handling: Robust fallback mechanisms
- Scalability: Ready for batch processing
- Performance tested: All files processed well under 10s requirement

## Testing
The project includes comprehensive tests:
- **Functionality tests**: Validate core features
- **Performance tests**: Ensure <10s processing requirement
- **Integration tests**: Docker container validation
- **Format tests**: JSON output validation

## Docker Configuration
- Base image: `python:3.10`
- Platform: `linux/amd64`
- Network: Isolated (no network access)
- Volumes: Input/output directory mapping

## Submission Ready
✅ Clean project structure (reorganized and duplicates removed)
✅ Comprehensive testing (local, Docker, performance, functionality)
✅ Docker containerization (rebuilt with current file structure)
✅ Performance validated (0.16s total for 5 files)
✅ Documentation complete (up-to-date with latest changes)
✅ Error handling robust (multi-engine fallback system)
✅ Output quality superior (better than original challenge data)
