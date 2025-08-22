@echo off
echo ========================================
echo FileRenamerTool Import Validation
echo ========================================
echo.

echo [1/3] Running quick import test...
python quick_import_test.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Quick test failed! Check the errors above.
    pause
    exit /b 1
)

echo.
echo [2/3] Running full import validation...
python import_validator.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Full validation failed! Check the errors above.
    pause
    exit /b 1
)

echo.
echo [3/3] Testing application startup...
python -c "from app_ui import App; print('✓ Application can be imported successfully')"
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application import test failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ All tests passed! Ready for packaging.
echo ========================================
echo.
echo Next steps:
echo 1. Run: pyinstaller --onefile --windowed main.py
echo 2. Test the generated executable
echo.
pause 