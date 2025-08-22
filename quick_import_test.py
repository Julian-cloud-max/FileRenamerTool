#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Import Test for FileRenamerTool
Fast validation of critical dependencies before packaging.
"""

import sys
import os

def quick_test():
    """Quick test of essential imports."""
    print("🔍 Quick Import Test for FileRenamerTool")
    print("=" * 50)
    
    tests = [
        ("customtkinter", "Main CustomTkinter"),
        ("tkinter", "Tkinter"),
        ("tkinter.filedialog", "File dialog"),
        ("tkinter.messagebox", "Message box"),
        ("os", "OS operations"),
        ("json", "JSON handling"),
        ("re", "Regular expressions"),
    ]
    
    failed = []
    
    for module, desc in tests:
        try:
            __import__(module)
            print(f"✓ {module} - {desc}")
        except ImportError as e:
            print(f"✗ {module} - {desc} - {e}")
            failed.append(module)
        except Exception as e:
            print(f"✗ {module} - {desc} - Unexpected: {e}")
            failed.append(module)
    
    # Test customtkinter resources
    try:
        import customtkinter
        import pkg_resources
        ctk_package = pkg_resources.get_distribution('customtkinter')
        ctk_path = ctk_package.location
        font_path = os.path.join(ctk_path, 'customtkinter', 'assets', 'fonts')
        
        if os.path.exists(font_path):
            print(f"✓ CustomTkinter fonts directory exists")
        else:
            print(f"✗ CustomTkinter fonts directory missing")
            failed.append("customtkinter_fonts")
    except Exception as e:
        print(f"✗ CustomTkinter resources check failed: {e}")
        failed.append("customtkinter_resources")
    
    # Test application imports
    try:
        from app_ui import App
        print("✓ Application module imports successfully")
    except Exception as e:
        print(f"✗ Application import failed: {e}")
        failed.append("app_ui")
    
    print("\n" + "=" * 50)
    if not failed:
        print("🎉 All tests passed! Ready for packaging.")
        return True
    else:
        print(f"⚠️  {len(failed)} tests failed: {', '.join(failed)}")
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1) 