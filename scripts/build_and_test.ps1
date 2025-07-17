# Adobe India Hackathon Round 1A - Build and Test Script (PowerShell)
# This script builds the Docker image and runs comprehensive tests

Write-Host "🚀 Adobe India Hackathon - Round 1A: PDF Outline Extractor" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green

# Check if Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed or not available in PATH" -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully" -ForegroundColor Green

# Create test directories
Write-Host "📁 Setting up test directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "test_input" -Force | Out-Null
New-Item -ItemType Directory -Path "test_output" -Force | Out-Null

# Copy sample PDFs for testing
if (Test-Path "Dataset/Challenge _1(a)/Datasets/Pdfs") {
    Copy-Item "Dataset/Challenge _1(a)/Datasets/Pdfs/*.pdf" -Destination "test_input/"
    Write-Host "✅ Copied sample PDFs from Dataset to test_input/" -ForegroundColor Green
} elseif (Test-Path "input") {
    Copy-Item "input/*.pdf" -Destination "test_input/"
    Write-Host "✅ Copied sample PDFs from input/ to test_input/" -ForegroundColor Green
} else {
    Write-Host "⚠️  No sample PDFs found. Please add PDFs to test_input/ directory" -ForegroundColor Yellow
    Write-Host "Expected locations: Dataset/Challenge _1(a)/Datasets/Pdfs or input/" -ForegroundColor Yellow
    exit 1
}

# Run the container
Write-Host "🏃 Running PDF outline extractor in Docker..." -ForegroundColor Yellow
$currentDir = Get-Location
docker run --rm `
    -v "${currentDir}/test_input:/app/input" `
    -v "${currentDir}/test_output:/app/output" `
    --network none `
    pdf-outline-extractor:latest

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Docker processing completed successfully!" -ForegroundColor Green
    Write-Host "📊 Results:" -ForegroundColor Cyan
    Write-Host "----------" -ForegroundColor Cyan
    
    # Show results summary
    $jsonFiles = Get-ChildItem "test_output/*.json" -ErrorAction SilentlyContinue
    if ($jsonFiles) {
        foreach ($file in $jsonFiles) {
            Write-Host "📄 $($file.Name)" -ForegroundColor Cyan
            try {
                $content = Get-Content $file.FullName | ConvertFrom-Json
                Write-Host "  📝 Title: $($content.title)" -ForegroundColor White
                Write-Host "  📋 Headings: $($content.outline.Count)" -ForegroundColor White
                Write-Host ""
            } catch {
                Write-Host "  ❌ Error reading JSON file" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "⚠️  No JSON files generated" -ForegroundColor Yellow
    }
    
    Write-Host "📁 Full results available in: test_output/" -ForegroundColor Cyan
} else {
    Write-Host "❌ Docker container execution failed" -ForegroundColor Red
    exit 1
}

# Clean up test directories
Write-Host "🧹 Cleaning up test directories..." -ForegroundColor Yellow
Remove-Item -Path "test_input", "test_output" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "🎉 Build and test completed successfully!" -ForegroundColor Green
Write-Host "🐳 Docker image 'pdf-outline-extractor:latest' is ready for submission" -ForegroundColor Cyan
