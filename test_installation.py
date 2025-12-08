#!/usr/bin/env python
"""
Comprehensive Installation and Environment Test Script

This script performs end-to-end validation of the installation pipeline,
including build tools, dependencies, and environment consistency.

Usage:
    python test_installation.py [--verbose]
"""

import sys
import os
import subprocess
import platform
from typing import Dict, List, Tuple, Optional

# Test configuration
MIN_PIP_VERSION = "23.0"
MIN_SETUPTOOLS_VERSION = "65.0"
MIN_WHEEL_VERSION = "0.40.0"
SUPPORTED_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
REQUIRED_PACKAGES = {
    "pygame": "2.6.1",
    "streamlit": "1.28.0",
    "Pillow": "10.0.0"
}


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}{text}{Colors.END}")
    print("=" * 70)


def print_success(text: str) -> None:
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {text}")


def print_error(text: str) -> None:
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {text}")


def print_warning(text: str) -> None:
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")


def print_info(text: str) -> None:
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {text}")


def compare_version(version: str, min_version: str) -> bool:
    """Compare version strings (simple semantic versioning)"""
    try:
        v_parts = [int(x) for x in version.split('.')[:3]]
        m_parts = [int(x) for x in min_version.split('.')[:3]]
        
        # Pad to same length
        while len(v_parts) < 3:
            v_parts.append(0)
        while len(m_parts) < 3:
            m_parts.append(0)
        
        return v_parts >= m_parts
    except (ValueError, AttributeError):
        return False


def test_python_version() -> bool:
    """Test Python version compatibility"""
    print_header("Python Version Check")
    
    version = platform.python_version()
    major_minor = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    print_info(f"Python version: {version}")
    print_info(f"Python implementation: {platform.python_implementation()}")
    print_info(f"Python executable: {sys.executable}")
    
    # Check if version is supported
    if major_minor in SUPPORTED_PYTHON_VERSIONS:
        print_success(f"Python {major_minor} is officially supported")
        
        # Special notes for specific versions
        if major_minor == "3.13":
            print_warning("Python 3.13 requires pygame 2.6.1+")
        elif major_minor == "3.12":
            print_success("Python 3.12 is the recommended version")
        elif major_minor in ["3.8", "3.9", "3.10", "3.11"]:
            print_success(f"Python {major_minor} is fully supported")
        
        return True
    else:
        print_error(f"Python {major_minor} is not in the supported versions list")
        print_info(f"Supported versions: {', '.join(SUPPORTED_PYTHON_VERSIONS)}")
        print_info("Recommended: Python 3.12")
        return False


def test_build_tools() -> bool:
    """Test pip, setuptools, and wheel versions"""
    print_header("Build Tools Check")
    
    all_passed = True
    
    # Test pip
    try:
        import pip
        pip_version = pip.__version__
        print_info(f"pip version: {pip_version}")
        
        if compare_version(pip_version, MIN_PIP_VERSION):
            print_success(f"pip {pip_version} >= {MIN_PIP_VERSION}")
        else:
            print_warning(f"pip {pip_version} < {MIN_PIP_VERSION} (recommended minimum)")
            print_info("Consider upgrading: pip install --upgrade pip")
            all_passed = False
    except Exception as e:
        print_error(f"Failed to check pip: {e}")
        all_passed = False
    
    # Test setuptools
    try:
        import setuptools
        setuptools_version = setuptools.__version__
        print_info(f"setuptools version: {setuptools_version}")
        
        if compare_version(setuptools_version, MIN_SETUPTOOLS_VERSION):
            print_success(f"setuptools {setuptools_version} >= {MIN_SETUPTOOLS_VERSION}")
        else:
            print_warning(f"setuptools {setuptools_version} < {MIN_SETUPTOOLS_VERSION} (recommended minimum)")
            print_info("Consider upgrading: pip install --upgrade setuptools")
            all_passed = False
    except Exception as e:
        print_error(f"Failed to check setuptools: {e}")
        all_passed = False
    
    # Test wheel
    try:
        import wheel
        wheel_version = wheel.__version__
        print_info(f"wheel version: {wheel_version}")
        
        if compare_version(wheel_version, MIN_WHEEL_VERSION):
            print_success(f"wheel {wheel_version} >= {MIN_WHEEL_VERSION}")
        else:
            print_warning(f"wheel {wheel_version} < {MIN_WHEEL_VERSION} (recommended minimum)")
            print_info("Consider upgrading: pip install --upgrade wheel")
            all_passed = False
    except Exception as e:
        print_error(f"Failed to check wheel: {e}")
        all_passed = False
    
    return all_passed


def test_pygame_installation() -> bool:
    """Test pygame installation and SDL support"""
    print_header("pygame Installation Check")
    
    try:
        import pygame
        
        print_success("pygame imported successfully")
        print_info(f"pygame version: {pygame.version.ver}")
        print_info(f"SDL version: {pygame.version.SDL}")
        
        # Check pygame version
        if pygame.version.ver == REQUIRED_PACKAGES["pygame"]:
            print_success(f"pygame version matches requirement ({REQUIRED_PACKAGES['pygame']})")
        elif compare_version(pygame.version.ver, REQUIRED_PACKAGES["pygame"]):
            print_warning(f"pygame {pygame.version.ver} is newer than requirement {REQUIRED_PACKAGES['pygame']}")
            print_info("This is usually fine, but may have untested behavior")
        else:
            print_error(f"pygame {pygame.version.ver} < {REQUIRED_PACKAGES['pygame']} (required)")
            return False
        
        # Test pygame initialization in headless mode
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        pygame.init()
        print_success("pygame.init() successful (headless mode)")
        
        # Test display creation
        screen = pygame.display.set_mode((100, 100))
        if screen is not None:
            print_success("pygame display initialized successfully")
            print_info(f"Display surface type: {type(screen)}")
        else:
            print_error("Failed to create pygame display surface")
            return False
        
        pygame.quit()
        
        # Check SDL version
        sdl_version = pygame.version.SDL
        print_info(f"SDL version: {sdl_version[0]}.{sdl_version[1]}.{sdl_version[2]}")
        
        if sdl_version[0] == 2 and sdl_version[1] >= 0:
            print_success("SDL2 version is compatible")
        else:
            print_warning("SDL version may be incompatible")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import pygame: {e}")
        print_info("Install with: pip install pygame==2.6.1")
        return False
    except Exception as e:
        print_error(f"pygame test failed: {e}")
        return False


def test_streamlit_installation() -> bool:
    """Test streamlit installation"""
    print_header("streamlit Installation Check")
    
    try:
        import streamlit
        
        print_success("streamlit imported successfully")
        print_info(f"streamlit version: {streamlit.__version__}")
        
        # Check streamlit version
        min_version = REQUIRED_PACKAGES["streamlit"]
        if compare_version(streamlit.__version__, min_version):
            print_success(f"streamlit {streamlit.__version__} >= {min_version}")
        else:
            print_warning(f"streamlit {streamlit.__version__} < {min_version} (recommended)")
            print_info("Consider upgrading: pip install --upgrade streamlit")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import streamlit: {e}")
        print_info("Install with: pip install streamlit>=1.28.0")
        return False
    except Exception as e:
        print_error(f"streamlit test failed: {e}")
        return False


def test_pillow_installation() -> bool:
    """Test Pillow installation"""
    print_header("Pillow Installation Check")
    
    try:
        from PIL import Image, ImageDraw
        import PIL
        
        print_success("Pillow imported successfully")
        print_info(f"Pillow version: {PIL.__version__}")
        
        # Check Pillow version
        min_version = REQUIRED_PACKAGES["Pillow"]
        if compare_version(PIL.__version__, min_version):
            print_success(f"Pillow {PIL.__version__} >= {min_version}")
        else:
            print_warning(f"Pillow {PIL.__version__} < {min_version} (recommended)")
            print_info("Consider upgrading: pip install --upgrade Pillow")
        
        # Test image creation
        img = Image.new('RGB', (100, 100), color='red')
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 90, 90], fill='blue')
        print_success("Pillow image creation and drawing works")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import Pillow: {e}")
        print_info("Install with: pip install Pillow>=10.0.0")
        return False
    except Exception as e:
        print_error(f"Pillow test failed: {e}")
        return False


def test_game_modules() -> bool:
    """Test game module imports"""
    print_header("Game Modules Check")
    
    all_passed = True
    
    # Test pygame version
    try:
        from simpsons_arcade import Character, Player, Enemy, Game, GameState
        print_success("simpsons_arcade.py imports successfully")
        
        # Test player creation
        player = Player(100, 100, (0, 0, 255), "Homer", "Homer")
        print_info(f"Created test player: {player.name} (Attack: {player.attack_power}, Health: {player.max_health})")
        print_success("pygame version game logic works")
        
    except ImportError as e:
        print_error(f"Failed to import simpsons_arcade: {e}")
        all_passed = False
    except Exception as e:
        print_error(f"simpsons_arcade test failed: {e}")
        all_passed = False
    
    # Test streamlit version
    try:
        from streamlit_simpsons_arcade import Character as StCharacter, Player as StPlayer
        print_success("streamlit_simpsons_arcade.py imports successfully")
        
        # Test player creation
        player = StPlayer(100, 100, (255, 255, 0), "Bart", "Bart")
        print_info(f"Created test player: {player.name} (Attack: {player.attack_power}, Health: {player.max_health})")
        print_success("Streamlit version game logic works")
        
    except ImportError as e:
        print_error(f"Failed to import streamlit_simpsons_arcade: {e}")
        all_passed = False
    except Exception as e:
        print_error(f"streamlit_simpsons_arcade test failed: {e}")
        all_passed = False
    
    return all_passed


def test_system_dependencies() -> bool:
    """Test system SDL2 dependencies (optional)"""
    print_header("System SDL2 Dependencies Check (Optional)")
    
    print_info("Checking for system SDL2 libraries...")
    print_info("Note: These are optional when using pre-built pygame wheels")
    
    # Try to find sdl2-config
    try:
        result = subprocess.run(['sdl2-config', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_success(f"sdl2-config found: {result.stdout.strip()}")
            print_info("System SDL2 libraries are available")
            return True
        else:
            print_info("sdl2-config not found")
            print_info("This is OK - pygame wheels include SDL2 libraries")
            return True
    except FileNotFoundError:
        print_info("sdl2-config not found")
        print_info("This is OK - pygame wheels include SDL2 libraries")
        return True
    except Exception as e:
        print_info(f"Could not check sdl2-config: {e}")
        print_info("This is OK - pygame wheels include SDL2 libraries")
        return True


def test_platform_info() -> None:
    """Display platform information"""
    print_header("Platform Information")
    
    print_info(f"Operating System: {platform.system()}")
    print_info(f"OS Release: {platform.release()}")
    print_info(f"OS Version: {platform.version()}")
    print_info(f"Machine: {platform.machine()}")
    print_info(f"Processor: {platform.processor()}")
    
    if platform.system() == "Linux":
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('PRETTY_NAME'):
                        print_info(f"Linux Distribution: {line.split('=')[1].strip().strip('\"')}")
                        break
        except:
            pass


def test_environment_variables() -> None:
    """Check relevant environment variables"""
    print_header("Environment Variables Check")
    
    env_vars = [
        'SDL_VIDEODRIVER',
        'SDL_AUDIODRIVER',
        'PYGAME_HIDE_SUPPORT_PROMPT',
        'STREAMLIT_SERVER_PORT',
    ]
    
    for var in env_vars:
        value = os.environ.get(var)
        if value:
            print_info(f"{var}={value}")
        else:
            print_info(f"{var}: not set")


def run_all_tests(verbose: bool = False) -> bool:
    """Run all tests and return overall success"""
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}ArcadeClassics - Installation Environment Test Suite{Colors.END}")
    print("=" * 70)
    
    results = []
    
    # Platform info (always passes)
    test_platform_info()
    
    # Run all tests
    results.append(("Python Version", test_python_version()))
    results.append(("Build Tools", test_build_tools()))
    results.append(("pygame", test_pygame_installation()))
    results.append(("streamlit", test_streamlit_installation()))
    results.append(("Pillow", test_pillow_installation()))
    results.append(("Game Modules", test_game_modules()))
    results.append(("System SDL2", test_system_dependencies()))
    
    if verbose:
        test_environment_variables()
    
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
        print_success("All tests passed! Environment is ready.")
        print_info("\nNext steps:")
        print_info("  - Run the game: streamlit run streamlit_simpsons_arcade.py")
        print_info("  - Or: python simpsons_arcade.py")
        print_info("  - Run unit tests: python test_simpsons_arcade.py")
        return True
    else:
        print_error("Some tests failed. Please fix the issues above.")
        print_info("\nRecommended actions:")
        print_info("  1. Update build tools: pip install --upgrade pip setuptools wheel")
        print_info("  2. Reinstall dependencies: pip install -r requirements.txt")
        print_info("  3. Check BUILD_REQUIREMENTS.md for detailed troubleshooting")
        return False


def main():
    """Main entry point"""
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    try:
        success = run_all_tests(verbose=verbose)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
