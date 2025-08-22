# FileRenamerTool Build Script
# Automated packaging with validation

param(
    [switch]$SkipValidation,
    [switch]$Debug,
    [switch]$Console,
    [string]$Icon = ""
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FileRenamerTool Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: main.py not found. Please run this script from the project directory." -ForegroundColor Red
    exit 1
}

# Step 1: Import Validation (unless skipped)
if (-not $SkipValidation) {
    Write-Host "[1/4] Running import validation..." -ForegroundColor Yellow
    
    $validationResult = python quick_import_test.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Import validation failed! Please fix the issues before packaging." -ForegroundColor Red
        Write-Host "Run 'python import_validator.py' for detailed information." -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "✅ Import validation passed!" -ForegroundColor Green
} else {
    Write-Host "[1/4] Skipping import validation..." -ForegroundColor Yellow
}

# Step 2: Clean previous builds
Write-Host "[2/4] Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
    Write-Host "✓ Removed build directory" -ForegroundColor Green
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue
    Write-Host "✓ Removed dist directory" -ForegroundColor Green
}
if (Test-Path "*.spec") {
    Get-ChildItem "*.spec" | Where-Object { $_.Name -ne "FileRenamerTool_optimized.spec" } | Remove-Item -Force
    Write-Host "✓ Cleaned old spec files" -ForegroundColor Green
}

# Step 3: Build with PyInstaller
Write-Host "[3/4] Building with PyInstaller..." -ForegroundColor Yellow

# Determine console setting
$consoleFlag = if ($Console) { "--console" } else { "--windowed" }

# Determine debug setting
$debugFlag = if ($Debug) { "--debug=all" } else { "" }

# Build icon flag
$iconFlag = if ($Icon -and (Test-Path $Icon)) { "--icon=$Icon" } else { "" }

# Choose spec file based on parameters
$specFile = if ($Debug -or $Console) { "FileRenamerTool_debug.spec" } else { "FileRenamerTool_optimized.spec" }

# Build command (when using .spec file, don't use conflicting options)
$buildCmd = "pyinstaller --clean $specFile"

Write-Host "Running: $buildCmd" -ForegroundColor Gray
$buildResult = Invoke-Expression $buildCmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ PyInstaller build failed!" -ForegroundColor Red
    Write-Host "Error output:" -ForegroundColor Red
    Write-Host $buildResult -ForegroundColor Red
    exit 1
}

Write-Host "✅ PyInstaller build completed!" -ForegroundColor Green

# Step 4: Verify the build
Write-Host "[4/4] Verifying the build..." -ForegroundColor Yellow

$exeName = if ($Debug -or $Console) { "FileRenamerTool_debug.exe" } else { "FileRenamerTool.exe" }
$exePath = "dist\$exeName"
if (Test-Path $exePath) {
    $fileSize = (Get-Item $exePath).Length
    $fileSizeMB = [math]::Round($fileSize / 1MB, 2)
    Write-Host "✅ Executable created successfully!" -ForegroundColor Green
    Write-Host "📁 Location: $exePath" -ForegroundColor Cyan
    Write-Host "📏 Size: $fileSizeMB MB" -ForegroundColor Cyan
    
    # Test if executable can start (basic test)
    Write-Host "🧪 Testing executable startup..." -ForegroundColor Yellow
    try {
        $process = Start-Process -FilePath $exePath -ArgumentList "--test" -PassThru -WindowStyle Hidden
        Start-Sleep -Seconds 2
        if (-not $process.HasExited) {
            $process.Kill()
            Write-Host "✅ Executable starts successfully!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Executable started but exited quickly (this might be normal)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Could not test executable startup: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Executable not found at expected location!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 Build completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "  • Executable: $exePath" -ForegroundColor White
Write-Host "  • Size: $fileSizeMB MB" -ForegroundColor White
Write-Host "  • Console mode: $Console" -ForegroundColor White
Write-Host "  • Debug mode: $Debug" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Test the executable manually" -ForegroundColor White
Write-Host "  2. Distribute the executable to users" -ForegroundColor White
Write-Host "  3. If issues occur, run with --Console flag for debugging" -ForegroundColor White
Write-Host ""

# Optional: Open the dist folder
$openFolder = Read-Host "Open dist folder? (y/n)"
if ($openFolder -eq "y" -or $openFolder -eq "Y") {
    Start-Process "explorer.exe" -ArgumentList "dist"
} 