# Quick Test Runner for Adobe India Hackathon Round 1A
# This script runs quick tests without Docker

Write-Host "⚡ Adobe India Hackathon - Round 1A: Quick Test Runner" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green

# Check if virtual environment Python is available
if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "❌ Virtual environment Python is not available" -ForegroundColor Red
    exit 1
}

# Run local solution
Write-Host "🏃 Running local solution..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe scripts/run_solution.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Local solution failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Local solution completed successfully!" -ForegroundColor Green

# Run functionality tests
Write-Host "🧪 Running functionality tests..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe tests/test_local.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Functionality tests failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Functionality tests passed!" -ForegroundColor Green

# Run performance tests
Write-Host "⏱️  Running performance tests..." -ForegroundColor Yellow
.\.venv\Scripts\python.exe tests/test_performance.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Performance tests failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Performance tests passed!" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 All tests completed successfully!" -ForegroundColor Green
Write-Host "🚀 Ready for Docker build and submission testing" -ForegroundColor Cyan
