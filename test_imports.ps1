# FileRenamerTool Import Validation Script
# PowerShell version

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FileRenamerTool Import Validation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 1: Quick import test
Write-Host "[1/3] Running quick import test..." -ForegroundColor Yellow
$quickResult = python quick_import_test.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Quick test failed! Check the errors above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/3] Running full import validation..." -ForegroundColor Yellow
$fullResult = python import_validator.py
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Full validation failed! Check the errors above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/3] Testing application startup..." -ForegroundColor Yellow
$appResult = python -c "from app_ui import App; print('✓ Application can be imported successfully')"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Application import test failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ All tests passed! Ready for packaging." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: pyinstaller --onefile --windowed main.py" -ForegroundColor White
Write-Host "2. Test the generated executable" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue" 