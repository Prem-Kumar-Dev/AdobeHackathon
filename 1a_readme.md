Here is your polished and enhanced `README.md` for **Round 1A** of the Adobe India Hackathon:

---

# Adobe India Hackathon: Connecting the Dots

## Round 1A: Understand Your Document

---

### 🧠 Challenge Mission

Your mission is to build a system that processes a raw PDF file and extracts a **structured outline**. This includes identifying the **Title** and hierarchical **headings** (H1, H2, H3), and organizing them into a clean, machine-readable format.

This outline acts as the foundational "brain" for the subsequent stages of the hackathon.

---

### 🌍 Why It Matters

PDFs are the global standard for sharing documents — but they are not natively machine-readable in a structured way. By building an outline extractor, you enable smarter, more interactive document experiences such as:

* Semantic search
* Context-aware recommendations
* Automated insight generation

This is the first step toward redefining how we understand and interact with knowledge.

---

### 🔨 What You Need to Build

Your solution should:

* Accept **a PDF file** (up to 50 pages) as input.
* Extract:

  * Document **Title**
  * **Headings** (H1, H2, H3), with:

    * Heading level
    * Text content
    * Page number
* Output a **valid JSON file** with the extracted data.

> 📁 Your container must read all `.pdf` files from `/app/input` and write `.json` files to `/app/output`.

---

### 📄 Expected JSON Output Format

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

### 🐳 Docker & Execution Requirements

* **Architecture**: Must support `linux/amd64` (`x86_64`)
* **Dependencies**: No GPU dependencies, must work **fully offline**
* **Model Size**: ≤ 200MB (if using a model)

#### Build Command

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

#### Run Command

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:somerandomidentifier
```

---

### 🧪 Example Usage

```bash
# Step 1: Prepare folders
mkdir input output
cp sample.pdf input/

# Step 2: Build Docker image
docker build --platform linux/amd64 -t pdf-outline-extractor .

# Step 3: Run your solution
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor

# Step 4: View the result
cat output/sample.json
```

---

### ⏱️ Constraints

| Constraint           | Requirement                    |
| -------------------- | ------------------------------ |
| Execution Time       | ≤ 10 seconds for a 50-page PDF |
| Model Size (if used) | ≤ 200MB                        |
| Network              | **No internet access allowed** |
| Runtime              | CPU-only, 8 CPUs + 16 GB RAM   |

---

### 🏆 Scoring Criteria

| Criteria                                          | Max Points |
| ------------------------------------------------- | ---------- |
| Heading Detection Accuracy (Precision/Recall)     | 25         |
| Performance (Execution Time & Model Size)         | 10         |
| **Bonus**: Multilingual Handling (e.g., Japanese) | 10         |
| **Total**                                         | **45**     |

---

### 📦 Submission Checklist

* ✅ Git project with a `Dockerfile` at the root
* ✅ A working `Dockerfile` with all dependencies
* ✅ A `README.md` that explains:

  * Your technical approach
  * Any models or libraries used
  * Instructions to build and run your solution

---

### 💡 Pro Tips

* Don’t rely **only on font size** to determine heading levels — real-world PDFs vary.
* Test your code on a **variety of PDFs**, from academic papers to reports.
* Write **modular code** — you’ll need it again in **Round 1B**.
* If you're supporting **multilingual content**, add a short note on it for reviewers.

---

### 🚫 What Not to Do

* ❌ Don’t hardcode heading logic for a specific file
* ❌ Don’t make **any API or internet calls**
* ❌ Don’t exceed the runtime or model size limits

---

Let me know if you also want a sample `approach_explanation.md` or code starter template!
