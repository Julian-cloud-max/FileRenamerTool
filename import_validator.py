#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import Validator Script for FileRenamerTool
This script validates all imports that might be needed during runtime.
Run this before packaging to catch import issues early.
"""

import sys
import os
import traceback
from typing import List, Dict, Tuple

def test_import(module_name: str, description: str = "") -> Tuple[bool, str]:
    """
    Test if a module can be imported successfully.
    
    Args:
        module_name: Name of the module to import
        description: Optional description of the module's purpose
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        __import__(module_name)
        return True, f"✓ {module_name} - {description}"
    except ImportError as e:
        return False, f"✗ {module_name} - {description} - Error: {e}"
    except Exception as e:
        return False, f"✗ {module_name} - {description} - Unexpected error: {e}"

def test_customtkinter_imports() -> List[Tuple[bool, str]]:
    """Test all customtkinter related imports."""
    results = []
    
    # Core customtkinter imports
    customtkinter_modules = [
        ("customtkinter", "Main customtkinter module"),
        ("customtkinter.windows", "Windows-specific customtkinter"),
        ("customtkinter.windows.widgets", "CustomTkinter widgets"),
        ("customtkinter.windows.widgets.core_rendering", "Core rendering"),
        ("customtkinter.windows.widgets.font", "Font handling"),
        ("customtkinter.windows.widgets.image", "Image handling"),
        ("customtkinter.windows.widgets.scaling", "Scaling utilities"),
        ("customtkinter.windows.widgets.color", "Color utilities"),
        ("customtkinter.windows.widgets.draw_engine", "Drawing engine"),
        ("customtkinter.windows.widgets.frame", "Frame widget"),
        ("customtkinter.windows.widgets.button", "Button widget"),
        ("customtkinter.windows.widgets.label", "Label widget"),
        ("customtkinter.windows.widgets.entry", "Entry widget"),
        ("customtkinter.windows.widgets.checkbox", "Checkbox widget"),
        ("customtkinter.windows.widgets.optionmenu", "Option menu widget"),
        ("customtkinter.windows.widgets.scrollable_frame", "Scrollable frame widget"),
        ("customtkinter.windows.ctk_input_dialog", "Input dialog"),
        ("customtkinter.windows.ctk_tk", "Tkinter integration"),
    ]
    
    for module_name, description in customtkinter_modules:
        results.append(test_import(module_name, description))
    
    return results

def test_tkinter_imports() -> List[Tuple[bool, str]]:
    """Test all tkinter related imports."""
    results = []
    
    tkinter_modules = [
        ("tkinter", "Main tkinter module"),
        ("tkinter.filedialog", "File dialog"),
        ("tkinter.messagebox", "Message box"),
        ("tkinter.ttk", "Themed tkinter widgets"),
        ("tkinter.font", "Font handling"),
        ("tkinter.colorchooser", "Color chooser"),
    ]
    
    for module_name, description in tkinter_modules:
        results.append(test_import(module_name, description))
    
    return results

def test_standard_library_imports() -> List[Tuple[bool, str]]:
    """Test standard library imports used in the application."""
    results = []
    
    stdlib_modules = [
        ("os", "Operating system interface"),
        ("json", "JSON encoding/decoding"),
        ("re", "Regular expressions"),
        ("sys", "System-specific parameters"),
        ("traceback", "Print or retrieve a stack traceback"),
        ("typing", "Support for type hints"),
    ]
    
    for module_name, description in stdlib_modules:
        results.append(test_import(module_name, description))
    
    return results

def test_customtkinter_resources() -> List[Tuple[bool, str]]:
    """Test if customtkinter resource files are accessible."""
    results = []
    
    try:
        import customtkinter
        import pkg_resources
        
        # Get customtkinter package location
        ctk_package = pkg_resources.get_distribution('customtkinter')
        ctk_path = ctk_package.location
        
        # Test resource directories
        resource_dirs = [
            os.path.join(ctk_path, 'customtkinter', 'assets', 'fonts'),
            os.path.join(ctk_path, 'customtkinter', 'assets', 'icons'),
            os.path.join(ctk_path, 'customtkinter', 'assets', 'themes'),
        ]
        
        for resource_dir in resource_dirs:
            if os.path.exists(resource_dir):
                results.append((True, f"✓ Resource directory exists: {resource_dir}"))
            else:
                results.append((False, f"✗ Resource directory missing: {resource_dir}"))
        
        # Test specific files
        font_file = os.path.join(ctk_path, 'customtkinter', 'assets', 'fonts', 'Roboto-Regular.ttf')
        if os.path.exists(font_file):
            results.append((True, f"✓ Font file exists: Roboto-Regular.ttf"))
        else:
            results.append((False, f"✗ Font file missing: Roboto-Regular.ttf"))
            
    except Exception as e:
        results.append((False, f"✗ Error checking customtkinter resources: {e}"))
    
    return results

def test_application_imports() -> List[Tuple[bool, str]]:
    """Test application-specific imports."""
    results = []
    
    # Test importing the main application modules
    try:
        from app_ui import App
        results.append((True, "✓ app_ui.App class imported successfully"))
    except Exception as e:
        results.append((False, f"✗ Failed to import app_ui.App: {e}"))
    
    try:
        import main
        results.append((True, "✓ main module imported successfully"))
    except Exception as e:
        results.append((False, f"✗ Failed to import main module: {e}"))
    
    return results

def test_runtime_imports() -> List[Tuple[bool, str]]:
    """Test imports that might be needed at runtime."""
    results = []
    
    # These are modules that might be imported dynamically or by customtkinter
    runtime_modules = [
        ("PIL", "Python Imaging Library (Pillow) - for image handling"),
        ("PIL.Image", "PIL Image module"),
        ("PIL.ImageTk", "PIL ImageTk module"),
        ("darkdetect", "Dark mode detection"),
        ("darkdetect.theme", "Dark mode theme detection"),
    ]
    
    for module_name, description in runtime_modules:
        results.append(test_import(module_name, description))
    
    return results

def run_all_tests() -> Dict[str, List[Tuple[bool, str]]]:
    """Run all import tests and return results."""
    print("🔍 Starting Import Validation for FileRenamerTool...")
    print("=" * 60)
    
    all_results = {}
    
    # Test standard library imports
    print("\n📚 Testing Standard Library Imports...")
    all_results['stdlib'] = test_standard_library_imports()
    
    # Test tkinter imports
    print("\n🎨 Testing Tkinter Imports...")
    all_results['tkinter'] = test_tkinter_imports()
    
    # Test customtkinter imports
    print("\n🎯 Testing CustomTkinter Imports...")
    all_results['customtkinter'] = test_customtkinter_imports()
    
    # Test customtkinter resources
    print("\n📁 Testing CustomTkinter Resources...")
    all_results['resources'] = test_customtkinter_resources()
    
    # Test application imports
    print("\n🚀 Testing Application Imports...")
    all_results['application'] = test_application_imports()
    
    # Test runtime imports
    print("\n⚡ Testing Runtime Imports...")
    all_results['runtime'] = test_runtime_imports()
    
    return all_results

def print_results(results: Dict[str, List[Tuple[bool, str]]]):
    """Print formatted test results."""
    print("\n" + "=" * 60)
    print("📊 IMPORT VALIDATION RESULTS")
    print("=" * 60)
    
    total_tests = 0
    passed_tests = 0
    
    for category, category_results in results.items():
        print(f"\n📋 {category.upper()}:")
        print("-" * 40)
        
        for success, message in category_results:
            total_tests += 1
            if success:
                passed_tests += 1
                print(f"  {message}")
            else:
                print(f"  {message}")
    
    print("\n" + "=" * 60)
    print(f"📈 SUMMARY: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All imports validated successfully! Ready for packaging.")
        return True
    else:
        print("⚠️  Some imports failed. Please fix the issues before packaging.")
        return False

def generate_pyinstaller_suggestions(results: Dict[str, List[Tuple[bool, str]]]) -> str:
    """Generate PyInstaller command suggestions based on test results."""
    suggestions = []
    
    # Check for customtkinter issues
    ctk_failures = [msg for success, msg in results.get('customtkinter', []) if not success]
    if ctk_failures:
        suggestions.append("--collect-all customtkinter")
    
    # Check for resource issues
    resource_failures = [msg for success, msg in results.get('resources', []) if not success]
    if resource_failures:
        suggestions.append("--add-data 'customtkinter/assets:customtkinter/assets'")
    
    # Check for runtime import issues
    runtime_failures = [msg for success, msg in results.get('runtime', []) if not success]
    if runtime_failures:
        for failure in runtime_failures:
            if "PIL" in failure:
                suggestions.append("--collect-all PIL")
            elif "darkdetect" in failure:
                suggestions.append("--collect-all darkdetect")
    
    if suggestions:
        print("\n💡 PYINSTALLER SUGGESTIONS:")
        print("-" * 40)
        base_cmd = "pyinstaller --onefile --windowed"
        print(f"Base command: {base_cmd}")
        print("Additional options:")
        for suggestion in suggestions:
            print(f"  {suggestion}")
        
        full_cmd = f"{base_cmd} {' '.join(suggestions)} main.py"
        print(f"\nFull command: {full_cmd}")
    
    return suggestions

def main():
    """Main function to run the import validator."""
    try:
        # Run all tests
        results = run_all_tests()
        
        # Print results
        success = print_results(results)
        
        # Generate PyInstaller suggestions
        generate_pyinstaller_suggestions(results)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Import validation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during import validation: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 