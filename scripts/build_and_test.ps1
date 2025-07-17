# Build and test script for Adobe India Hackathon Round 1A (PowerShell)

Write-Host "🚀 Adobe India Hackathon - Round 1A: PDF Outline Extractor" -ForegroundColor Green
Write-Host "=============================================================" -ForegroundColor Green

# Check if Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed or not available in PATH" -ForegroundColor Red
    exit 1
}

# Build the Docker image
Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker build --platform linux/amd64 -t pdf-analyzer .

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
    Write-Host "✅ Copied sample PDFs to test_input/" -ForegroundColor Green
} else {
    Write-Host "⚠️  No sample PDFs found. Please add PDFs to test_input/ directory" -ForegroundColor Yellow
    Write-Host "Expected path: Dataset/Challenge _1(a)/Datasets/Pdfs" -ForegroundColor Yellow
}

# Run the container
Write-Host "🏃 Running PDF outline extractor..." -ForegroundColor Yellow
$currentDir = Get-Location
docker run --rm -v "${currentDir}/test_input:/app/input" -v "${currentDir}/test_output:/app/output" --network none pdf-analyzer

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Processing completed successfully!" -ForegroundColor Green
    Write-Host "📊 Results:" -ForegroundColor Cyan
    Write-Host "----------" -ForegroundColor Cyan
    
    # Show results
    Get-ChildItem "test_output/*.json" | ForEach-Object {
        Write-Host "📄 $($_.Name)" -ForegroundColor Cyan
        Get-Content $_.FullName | Select-Object -First 10
        Write-Host ""
    }
    
    Write-Host "📁 Full results available in: test_output/" -ForegroundColor Cyan
} else {
    Write-Host "❌ Container execution failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Build and test completed!" -ForegroundColor Green
