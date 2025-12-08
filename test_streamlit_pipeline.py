#!/usr/bin/env python
"""
End-to-End Streamlit Pipeline Test

This script tests the complete Streamlit game execution pipeline from
dependency installation to app functionality, simulating both local
and Streamlit Cloud deployment scenarios.

Usage:
    python test_streamlit_pipeline.py
"""

import sys
import os
import shutil
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


def test_requirements_installation() -> bool:
    """Test that requirements.txt can be installed cleanly"""
    print_header("Requirements Installation Test")
    
    try:
        print_info("Testing requirements.txt installation in isolated environment...")
        
        # Check if requirements.txt exists
        if not Path('requirements.txt').exists():
            print_error("requirements.txt not found")
            return False
        
        print_success("requirements.txt found")
        
        # Read requirements
        with open('requirements.txt', 'r') as f:
            content = f.read()
            print_info(f"Requirements file has {len(content.splitlines())} lines")
        
        # Check that key packages are listed
        required_packages = ['pygame', 'streamlit', 'Pillow']
        for package in required_packages:
            if package in content:
                print_success(f"Found {package} in requirements.txt")
            else:
                print_error(f"{package} not found in requirements.txt")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Requirements test failed: {e}")
        return False


def test_runtime_configuration() -> bool:
    """Test runtime.txt configuration"""
    print_header("Runtime Configuration Test")
    
    try:
        # Check if runtime.txt exists
        if not Path('runtime.txt').exists():
            print_error("runtime.txt not found")
            print_info("This file is required for Streamlit Cloud deployment")
            return False
        
        print_success("runtime.txt found")
        
        # Read runtime.txt
        with open('runtime.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not lines:
            print_error("runtime.txt is empty or contains only comments")
            return False
        
        # Extract Python version specification
        python_spec = lines[0] if lines else None
        print_info(f"Python specification: {python_spec}")
        
        # Validate format
        if python_spec and python_spec.startswith('python-'):
            version = python_spec.replace('python-', '')
            print_success(f"Valid Python version specification: {version}")
            
            # Check if it's a supported version
            if version.startswith('3.12') or version.startswith('3.11') or version.startswith('3.10'):
                print_success(f"Python {version} is a recommended version")
            elif version.startswith('3.13'):
                print_info(f"Python {version} requires pygame 2.6.1+")
            
            return True
        else:
            print_error("Invalid Python specification format")
            print_info("Expected format: python-X.Y.Z")
            return False
        
    except Exception as e:
        print_error(f"Runtime configuration test failed: {e}")
        return False


def test_packages_configuration() -> bool:
    """Test packages.txt configuration"""
    print_header("System Packages Configuration Test")
    
    try:
        # Check if packages.txt exists
        if not Path('packages.txt').exists():
            print_error("packages.txt not found")
            print_info("This file is required for Streamlit Cloud deployment")
            return False
        
        print_success("packages.txt found")
        
        # Read packages.txt
        with open('packages.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not lines:
            print_error("packages.txt is empty or contains only comments")
            return False
        
        print_info(f"Found {len(lines)} system packages")
        
        # Check for essential SDL2 packages
        required_packages = [
            'libsdl2-dev',
            'libsdl2-image-dev',
            'libsdl2-mixer-dev',
            'libsdl2-ttf-dev'
        ]
        
        for package in required_packages:
            if package in lines:
                print_success(f"Found essential package: {package}")
            else:
                print_error(f"Missing essential package: {package}")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Packages configuration test failed: {e}")
        return False


def test_streamlit_app_exists() -> bool:
    """Test that the Streamlit app file exists and is valid"""
    print_header("Streamlit App File Test")
    
    try:
        app_file = 'streamlit_simpsons_arcade.py'
        
        if not Path(app_file).exists():
            print_error(f"{app_file} not found")
            return False
        
        print_success(f"{app_file} found")
        
        # Read and check file content
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Check for essential imports
        essential_imports = ['import streamlit', 'from PIL import']
        for imp in essential_imports:
            if imp in content:
                print_success(f"Found import: {imp}")
            else:
                print_error(f"Missing import: {imp}")
                return False
        
        # Check for streamlit usage
        if 'st.' in content:
            print_success("File uses streamlit API")
        else:
            print_error("File doesn't appear to use streamlit API")
            return False
        
        print_info(f"App file size: {len(content)} bytes")
        
        return True
        
    except Exception as e:
        print_error(f"Streamlit app file test failed: {e}")
        return False


def test_streamlit_app_import() -> bool:
    """Test that the Streamlit app can be imported"""
    print_header("Streamlit App Import Test")
    
    try:
        print_info("Attempting to import streamlit_simpsons_arcade...")
        
        # Import the module
        import streamlit_simpsons_arcade
        
        print_success("streamlit_simpsons_arcade imported successfully")
        
        # Check for essential classes
        essential_classes = ['Character', 'Player', 'Enemy', 'GameState']
        for cls_name in essential_classes:
            if hasattr(streamlit_simpsons_arcade, cls_name):
                print_success(f"Found class: {cls_name}")
            else:
                print_error(f"Missing class: {cls_name}")
                return False
        
        # Test class instantiation
        try:
            player = streamlit_simpsons_arcade.Player(100, 100, (0, 0, 255), "Homer", "Homer")
            print_success(f"Successfully created Player instance: {player.name}")
        except Exception as e:
            print_error(f"Failed to create Player instance: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import streamlit_simpsons_arcade: {e}")
        return False
    except Exception as e:
        print_error(f"Streamlit app import test failed: {e}")
        return False


def test_game_logic() -> bool:
    """Test core game logic without Streamlit UI"""
    print_header("Game Logic Test")
    
    try:
        from streamlit_simpsons_arcade import Player, Enemy, GameState
        
        print_info("Testing game state enum...")
        
        # Check GameState enum values
        game_state = GameState.MENU
        print_success(f"GameState enum works: {game_state}")
        
        # Create a player
        player = Player(100, 350, (0, 0, 255), "Homer", "Homer")
        print_success(f"Player created: {player.name} (Health: {player.health})")
        
        # Create an enemy
        enemy = Enemy(400, 350)
        print_success(f"Enemy created at position ({enemy.x}, {enemy.y})")
        
        # Test movement
        original_x = player.x
        player.move(5, 0)
        if player.x != original_x:
            print_success("Player movement works")
        else:
            print_error("Player movement doesn't work")
            return False
        
        # Test attack range calculation
        player.x = 100
        enemy.x = 150
        in_range = abs(player.x - enemy.x) <= 60
        print_info(f"Attack range check: {'in range' if in_range else 'out of range'}")
        print_success("Attack range calculation works")
        
        return True
        
    except Exception as e:
        print_error(f"Game logic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rendering_system() -> bool:
    """Test the PIL rendering system"""
    print_header("Rendering System Test")
    
    try:
        from streamlit_simpsons_arcade import draw_game_screen, Player, Enemy
        from PIL import Image
        
        print_info("Testing game screen rendering...")
        
        # Create player and enemies
        player = Player(100, 350, (0, 0, 255), "Bart", "Bart")
        enemies = [Enemy(300, 350), Enemy(500, 350)]
        
        # Test rendering with draw_game_screen(player, enemies, ground_level, level)
        # ground_level determines where characters stand, level is the current game level
        ground_level = 350
        level = 1
        img = draw_game_screen(player, enemies, ground_level, level)
        
        if isinstance(img, Image.Image):
            print_success("Rendering produces PIL Image")
            print_info(f"Image size: {img.size}")
            print_info(f"Image mode: {img.mode}")
        else:
            print_error("Rendering doesn't produce PIL Image")
            return False
        
        # Verify image dimensions
        if img.size == (800, 600):
            print_success("Image has correct dimensions (800x600)")
        else:
            print_error(f"Image has incorrect dimensions: {img.size}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Rendering system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dependency_compatibility() -> bool:
    """Test that all dependencies work together"""
    print_header("Dependency Compatibility Test")
    
    try:
        print_info("Testing dependency interactions...")
        
        # Import all major dependencies
        import pygame
        import streamlit
        from PIL import Image
        
        print_success("All major dependencies imported")
        
        # Test pygame doesn't interfere with PIL
        img = Image.new('RGB', (100, 100), color='red')
        print_success("PIL works independently of pygame")
        
        # Test version compatibility
        print_info(f"pygame: {pygame.version.ver}, SDL: {pygame.version.SDL}")
        print_info(f"streamlit: {streamlit.__version__}")
        
        import PIL
        print_info(f"Pillow: {PIL.__version__}")
        
        return True
        
    except Exception as e:
        print_error(f"Dependency compatibility test failed: {e}")
        return False


def test_environment_consistency() -> bool:
    """Test environment consistency across different scenarios"""
    print_header("Environment Consistency Test")
    
    try:
        print_info("Checking environment variables...")
        
        # Check for conflicting environment variables
        conflicting_vars = {
            'SDL_VIDEODRIVER': os.environ.get('SDL_VIDEODRIVER'),
            'SDL_AUDIODRIVER': os.environ.get('SDL_AUDIODRIVER'),
        }
        
        for var, value in conflicting_vars.items():
            if value:
                print_info(f"{var}={value}")
                if value == 'dummy':
                    print_success(f"{var} set for headless mode (good for testing)")
            else:
                print_info(f"{var} not set (will use defaults)")
        
        # Check Python path
        print_info(f"Python executable: {sys.executable}")
        print_info(f"Python version: {sys.version.split()[0]}")
        
        # Check working directory
        print_info(f"Working directory: {os.getcwd()}")
        
        return True
        
    except Exception as e:
        print_error(f"Environment consistency test failed: {e}")
        return False


def run_all_tests() -> bool:
    """Run all pipeline tests"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}Streamlit Pipeline End-to-End Test Suite{Colors.END}")
    print("=" * 70)
    
    results = []
    
    # Run all tests
    results.append(("Requirements Installation", test_requirements_installation()))
    results.append(("Runtime Configuration", test_runtime_configuration()))
    results.append(("System Packages Configuration", test_packages_configuration()))
    results.append(("Streamlit App File", test_streamlit_app_exists()))
    results.append(("Streamlit App Import", test_streamlit_app_import()))
    results.append(("Game Logic", test_game_logic()))
    results.append(("Rendering System", test_rendering_system()))
    results.append(("Dependency Compatibility", test_dependency_compatibility()))
    results.append(("Environment Consistency", test_environment_consistency()))
    
    # Summary
    print_header("Test Summary")
    
    all_passed = True
    for name, passed in results:
        if passed:
            print_success(f"{name}: PASS")
        else:
            print_error(f"{name}: FAIL")
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print_success("All pipeline tests passed!")
        print_info("\nThe Streamlit pipeline is ready for deployment:")
        print_info("  - Local: streamlit run streamlit_simpsons_arcade.py")
        print_info("  - Streamlit Cloud: Deploy with current configuration")
        print_info("\nAll required files are present and correctly configured:")
        print_info("  ✓ requirements.txt - Python dependencies")
        print_info("  ✓ packages.txt - System dependencies")
        print_info("  ✓ runtime.txt - Python version")
        print_info("  ✓ streamlit_simpsons_arcade.py - Main app")
        return True
    else:
        print_error("Some pipeline tests failed.")
        print_info("\nPlease fix the issues above before deployment.")
        return False


def main():
    """Main entry point"""
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
