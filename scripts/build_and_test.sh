#!/bin/bash
# Adobe India Hackathon Round 1A - Build and Test Script (Unix/Linux)

echo "🚀 Adobe India Hackathon - Round 1A: PDF Outline Extractor"
echo "============================================================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not available in PATH"
    exit 1
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

# Create test directories
echo "📁 Setting up test directories..."
mkdir -p test_input test_output

# Copy sample PDFs for testing
if [ -d "Dataset/Challenge _1(a)/Datasets/Pdfs" ]; then
    cp "Dataset/Challenge _1(a)/Datasets/Pdfs"/*.pdf test_input/
    echo "✅ Copied sample PDFs from Dataset to test_input/"
elif [ -d "input" ]; then
    cp input/*.pdf test_input/
    echo "✅ Copied sample PDFs from input/ to test_input/"
else
    echo "⚠️  No sample PDFs found. Please add PDFs to test_input/ directory"
    echo "Expected locations: Dataset/Challenge _1(a)/Datasets/Pdfs or input/"
    exit 1
fi

# Run the container
echo "🏃 Running PDF outline extractor in Docker..."
docker run --rm \
    -v "$(pwd)/test_input:/app/input" \
    -v "$(pwd)/test_output:/app/output" \
    --network none \
    pdf-outline-extractor:latest

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker processing completed successfully!"
    echo "📊 Results:"
    echo "----------"
    
    # Show results summary
    for json_file in test_output/*.json; do
        if [ -f "$json_file" ]; then
            echo "📄 $(basename "$json_file")"
            echo "  📝 Title: $(jq -r '.title' "$json_file" 2>/dev/null || echo 'Error reading title')"
            echo "  📋 Headings: $(jq '.outline | length' "$json_file" 2>/dev/null || echo 'Error reading headings')"
            echo ""
        fi
    done
    
    echo "📁 Full results available in: test_output/"
else
    echo "❌ Docker container execution failed"
    exit 1
fi

# Clean up test directories
echo "🧹 Cleaning up test directories..."
rm -rf test_input test_output

echo ""
echo "🎉 Build and test completed successfully!"
echo "🐳 Docker image 'pdf-outline-extractor:latest' is ready for submission"
