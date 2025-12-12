#!/usr/bin/env python
"""
Comprehensive Test Suite Runner

This script runs all test suites in the correct order to validate
the entire project including installation, dependencies, game logic,
and deployment readiness.

Usage:
    python run_all_tests.py [--verbose]
"""

import sys
import subprocess
from pathlib import Path


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{text}{Colors.END}")
    print("=" * 70)


def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {text}")


def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")


def run_test_script(script_name: str, description: str) -> bool:
    """Run a test script and return success status"""
    print_header(description)
    
    if not Path(script_name).exists():
        print_error(f"Test script not found: {script_name}")
        return False
    
    print_info(f"Running: {script_name}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print_success(f"{script_name} passed")
            return True
        else:
            print_error(f"{script_name} failed with exit code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print_error(f"{script_name} timed out")
        return False
    except Exception as e:
        print_error(f"Error running {script_name}: {e}")
        return False


def main():
    """Main test runner"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}ArcadeClassics - Comprehensive Test Suite{Colors.END}")
    print("=" * 70)
    print_info("Running all tests to validate installation and deployment readiness")
    
    # Define test suite
    test_suites = [
        ("test_installation.py", "Installation & Environment Tests"),
        ("test_streamlit_pipeline.py", "Streamlit Pipeline Tests"),
        ("test_simpsons_arcade.py", "Pygame Version Unit Tests"),
        ("test_streamlit_simpsons.py", "Streamlit Version Unit Tests"),
        ("verify_dependencies.py", "Dependency Verification"),
    ]
    
    results = []
    
    # Run all test suites
    for script, description in test_suites:
        success = run_test_script(script, description)
        results.append((description, success))
    
    # Summary
    print_header("Overall Test Summary")
    
    all_passed = True
    for description, passed in results:
        if passed:
            print_success(f"{description}: PASS")
        else:
            print_error(f"{description}: FAIL")
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print_success("All test suites passed!")
        print_info("\nThe project is ready for deployment:")
        print_info("  ✓ All dependencies installed correctly")
        print_info("  ✓ pygame and SDL2 working properly")
        print_info("  ✓ Streamlit integration validated")
        print_info("  ✓ Game logic tested and working")
        print_info("  ✓ Configuration files validated")
        print_info("\nNext steps:")
        print_info("  - Local testing: streamlit run streamlit_simpsons_arcade.py")
        print_info("  - Desktop version: python simpsons_arcade.py")
        print_info("  - Deploy to Streamlit Cloud with current configuration")
        return 0
    else:
        print_error("Some test suites failed!")
        print_info("\nPlease review the failures above and fix the issues.")
        print_info("See BUILD_REQUIREMENTS.md for troubleshooting guidance.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
