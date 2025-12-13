#!/usr/bin/env python
"""
Verification script to test SDL dependencies and pygame installation.
This script checks that:
1. pygame is installed correctly
2. SDL libraries are accessible
3. Both game versions can import successfully
"""

import sys

# Test constants
TEST_SCREEN_WIDTH = 100
TEST_SCREEN_HEIGHT = 100
TEST_PLAYER_X = 100
TEST_PLAYER_Y = 100
TEST_COLOR_BLUE = (0, 0, 255)
TEST_COLOR_RED = (255, 0, 0)
TEST_IMAGE_SIZE = (100, 100)
SDL_CONFIG_TIMEOUT = 5  # seconds

def test_pygame():
    """Test pygame and SDL installation"""
    print("=" * 60)
    print("Testing pygame and SDL Dependencies")
    print("=" * 60)
    
    try:
        import pygame
        print(f"✓ pygame imported successfully")
        print(f"  - pygame version: {pygame.version.ver}")
        print(f"  - SDL version: {pygame.version.SDL}")
        
        # Initialize pygame to test SDL
        pygame.init()
        print(f"✓ pygame.init() successful")
        
        # Test display (headless mode for CI)
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'
        
        pygame.display.set_mode((TEST_SCREEN_WIDTH, TEST_SCREEN_HEIGHT))
        print(f"✓ pygame display initialized (headless mode)")
        
        pygame.quit()
        return True
    except Exception as e:
        print(f"✗ pygame test failed: {e}")
        return False

def test_streamlit():
    """Test streamlit installation"""
    print("\n" + "=" * 60)
    print("Testing Streamlit Dependencies")
    print("=" * 60)
    
    try:
        import streamlit
        print(f"✓ streamlit imported successfully")
        print(f"  - streamlit version: {streamlit.__version__}")
        return True
    except Exception as e:
        print(f"✗ streamlit test failed: {e}")
        return False

def test_pillow():
    """Test Pillow installation"""
    print("\n" + "=" * 60)
    print("Testing Pillow Dependencies")
    print("=" * 60)
    
    try:
        from PIL import Image, ImageDraw
        import PIL
        print(f"✓ Pillow imported successfully")
        print(f"  - Pillow version: {PIL.__version__}")
        
        # Test creating an image
        img = Image.new('RGB', TEST_IMAGE_SIZE, color='red')
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 10, 90, 90], fill='blue')
        print(f"✓ Pillow image creation and drawing works")
        return True
    except Exception as e:
        print(f"✗ Pillow test failed: {e}")
        return False

def test_game_imports():
    """Test game module imports"""
    print("\n" + "=" * 60)
    print("Testing Game Module Imports")
    print("=" * 60)
    
    success = True
    
    # Test pygame version
    try:
        from simpsons_arcade import Character, Player, Enemy, Game, GameState
        print(f"✓ simpsons_arcade.py imports successfully")
        
        # Create a test player
        player = Player(TEST_PLAYER_X, TEST_PLAYER_Y, TEST_COLOR_BLUE, "Homer", "Homer")
        print(f"✓ Created pygame version player: {player.name} (Attack: {player.attack_power}, Health: {player.max_health})")
    except Exception as e:
        print(f"✗ simpsons_arcade.py import failed: {e}")
        success = False
    
    # Test streamlit version
    try:
        from streamlit_simpsons_arcade import Character as StCharacter, Player as StPlayer, Enemy as StEnemy, GameState as StGameState
        print(f"✓ streamlit_simpsons_arcade.py imports successfully")
        
        # Create a test player
        player = StPlayer(TEST_PLAYER_X, TEST_PLAYER_Y, TEST_COLOR_BLUE, "Bart", "Bart")
        print(f"✓ Created streamlit version player: {player.name} (Attack: {player.attack_power}, Health: {player.max_health})")
    except Exception as e:
        print(f"✗ streamlit_simpsons_arcade.py import failed: {e}")
        success = False
    
    return success

def test_sdl_config():
    """Check for SDL configuration issues"""
    print("\n" + "=" * 60)
    print("Testing SDL Configuration")
    print("=" * 60)
    
    import subprocess
    
    # Try to run sdl2-config if available
    try:
        result = subprocess.run(['sdl2-config', '--version'], 
                              capture_output=True, text=True, timeout=SDL_CONFIG_TIMEOUT)
        if result.returncode == 0:
            print(f"✓ sdl2-config found: {result.stdout.strip()}")
        else:
            print(f"  sdl2-config not found (OK - pygame wheels include SDL2)")
    except FileNotFoundError:
        print(f"  sdl2-config not found (OK - pygame wheels include SDL2)")
    except Exception as e:
        print(f"  Could not check sdl2-config: {e}")
    
    # Check if pygame is using bundled SDL
    import pygame
    print(f"  pygame is using SDL version: {pygame.version.SDL}")
    print(f"✓ SDL libraries are accessible to pygame")
    
    return True

def main():
    """Run all verification tests"""
    print("\n")
    print("*" * 60)
    print("SDL Dependency Verification Script")
    print("*" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("pygame", test_pygame()))
    results.append(("streamlit", test_streamlit()))
    results.append(("Pillow", test_pillow()))
    results.append(("game imports", test_game_imports()))
    results.append(("SDL config", test_sdl_config()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All dependency checks passed!")
        print("  The game is ready to run.")
        print("\nTo play:")
        print("  - Streamlit version: streamlit run streamlit_simpsons_arcade.py")
        print("  - Pygame version:    python simpsons_arcade.py")
        return 0
    else:
        print("\n✗ Some dependency checks failed.")
        print("  Please install missing dependencies:")
        print("    pip install -r requirements.txt")
        print("\n  If you see SDL errors, see DEPLOYMENT.md for platform-specific instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
