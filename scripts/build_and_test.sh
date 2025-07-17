#!/bin/bash
# Build and test script for Adobe India Hackathon Round 1A

echo "🚀 Adobe India Hackathon - Round 1A: PDF Outline Extractor"
echo "============================================================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not available in PATH"
    exit 1
fi

# Build the Docker image
echo "🔨 Building Docker image..."
docker build --platform linux/amd64 -t pdf-analyzer .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

# Create test directories
echo "📁 Setting up test directories..."
mkdir -p test_input test_output

# Copy sample PDFs for testing
if [ -d "../Dataset/Challenge _1(a)/Datasets/Pdfs" ]; then
    cp "../Dataset/Challenge _1(a)/Datasets/Pdfs"/*.pdf test_input/
    echo "✅ Copied sample PDFs to test_input/"
else
    echo "⚠️  No sample PDFs found. Please add PDFs to test_input/ directory"
    echo "Expected path: ../Dataset/Challenge _1(a)/Datasets/Pdfs"
fi

# Run the container
echo "🏃 Running PDF outline extractor..."
docker run --rm \
    -v "$(pwd)/test_input:/app/input" \
    -v "$(pwd)/test_output:/app/output" \
    --network none \
    pdf-analyzer

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Processing completed successfully!"
    echo "📊 Results:"
    echo "----------"
    
    # Show results
    for json_file in test_output/*.json; do
        if [ -f "$json_file" ]; then
            echo "📄 $(basename "$json_file")"
            head -10 "$json_file"
            echo ""
        fi
    done
    
    echo "📁 Full results available in: test_output/"
else
    echo "❌ Container execution failed"
    exit 1
fi

echo ""
echo "🎉 Build and test completed!"
