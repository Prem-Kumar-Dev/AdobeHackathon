````markdown
# 🧠 Adobe India Hackathon 2025 – Connecting the Dots

Welcome to the Adobe India Hackathon 2025. This project implements both Round 1A and Round 1B of the “Connecting the Dots” challenge.

## 📦 Objective

Build an intelligent, offline-compatible document analysis system with two phases:

- ✅ Round 1A: Extract structured outlines (Title, H1, H2, H3 + page number) from PDF documents.
- ✅ Round 1B: From a document collection and a given persona/task, extract and rank relevant sections and subsections using document understanding.

---

## 🧩 Round 1A – Understand Your Document

### 🎯 Goal

For each PDF in input/, extract:
- Title (first prominent heading)
- Headings with level (H1, H2, H3)
- Page number

Output each result as: output/filename.json

### 📝 Output Format

Example:
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 0 },
    { "level": "H2", "text": "What is AI?", "page": 1 },
    { "level": "H3", "text": "History of AI", "page": 2 }
  ]
}
````

### 🧪 Constraints (Round 1A)

| Constraint         | Requirement                      |
| ------------------ | -------------------------------- |
| Max Execution Time | ≤ 10 seconds (per 50-page PDF)   |
| Max Model Size     | ≤ 200MB (if any model is used)   |
| Runtime            | CPU only (no GPU), 8 vCPU, 16 GB |
| Internet Access    | Not allowed                      |
| Platform           | Must run on linux/amd64          |

### 🏆 Scoring (Round 1A)

| Metric                     | Points |
| -------------------------- | ------ |
| Heading Detection Accuracy | 25     |
| Performance (Time, Size)   | 10     |
| Multilingual Bonus         | 10     |
| Total                      | 45     |

---

## 🧠 Round 1B – Persona-Driven Document Intelligence

### 🎯 Goal

Given a persona + job description and multiple PDFs, extract and rank:

* Relevant sections
* Their page numbers and titles
* Relevant refined sub-sections and summaries

### 📥 Inputs

* PDFs in input/
* persona/persona.json:

```json
{
  "persona": "PhD Researcher in Computational Biology",
  "job_to_be_done": "Prepare a comprehensive literature review on graph neural networks"
}
```

Note: If persona.json is not present, assume Round 1A.

### 📝 Output Format

```json
{
  "metadata": {
    "documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher",
    "job": "Literature Review on GNNs",
    "timestamp": "2025-07-25T12:00:00Z"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page": 2,
      "section_title": "Graph Neural Networks in Drug Design",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Recent advances in GNN models...",
      "page": 2
    }
  ]
}
```

### 🧪 Constraints (Round 1B)

| Constraint      | Requirement             |
| --------------- | ----------------------- |
| Execution Time  | ≤ 60s for 3–5 PDFs      |
| Max Model Size  | ≤ 1GB                   |
| Runtime         | CPU only                |
| Internet Access | Not allowed             |
| Platform        | Must run on linux/amd64 |

### 🏆 Scoring (Round 1B)

| Metric                        | Points |
| ----------------------------- | ------ |
| Section Relevance             | 60     |
| Subsection Refinement Quality | 40     |
| Total                         | 100    |

---

## 🐳 Docker Instructions

Both rounds must be containerized.

### 📦 Docker Build

```bash
docker build --platform linux/amd64 -t pdf-analyzer .
```

### ▶️ Docker Run

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/persona:/app/persona \
  --network none \
  pdf-analyzer
```

The script should detect:

* Round 1A → if only PDFs in /input
* Round 1B → if persona/persona.json is also present

---

## 🧪 Testing & Validation

Run solution locally:

```bash
python scripts/run_solution.py
```

Test runners:

* Linux/macOS: ./scripts/build\_and\_test.sh
* Windows:     .\scripts\build\_and\_test.ps1

---

## ✅ Submission Checklist

* [x] Dockerfile that builds on linux/amd64
* [x] Fully offline solution
* [x] Output matches exact JSON schema
* [x] Works for both rounds
* [x] No hardcoding or network access
* [x] Code is modular and testable

---

🏁 Built with ❤️ for Adobe India Hackathon 2025

```

Let me know if you'd like:

- A matching approach_explanation.md
- Round 1B persona inference from dataset (optional spec)
- Separate markdowns for 1A and 1B
- Shell script or GitHub Action for validation

Happy hacking!
```
