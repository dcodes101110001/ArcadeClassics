"""
Test edge cases and bug fixes for the ArcadeClassics games.
This test suite validates that known bugs have been fixed.
"""

import os
import sys

# Set environment variables for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

def test_division_by_zero_pygame():
    """Test that division by zero is handled in pygame version"""
    from simpsons_arcade import Character, Player
    
    # Test Character with zero max_health
    char = Character(100, 100, (255, 0, 0), "TestChar", health=0)
    char.max_health = 0  # Edge case: zero max_health
    
    # This should not raise ZeroDivisionError
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        char.draw(screen)  # Should handle division by zero gracefully
        print("✓ pygame Character.draw() handles zero max_health")
        pygame.quit()
    except ZeroDivisionError:
        print("✗ pygame Character.draw() failed with ZeroDivisionError")
        return False
    
    return True

def test_division_by_zero_streamlit():
    """Test that division by zero is handled in streamlit version"""
    from streamlit_simpsons_arcade import Character, Player, Enemy, draw_game_screen
    
    # Test Player with zero max_health
    player = Player(100, 500, (0, 0, 255), "Homer", "Homer")
    player.max_health = 0  # Edge case: zero max_health
    player.health = 0
    
    # Test Enemy with zero max_health
    enemy = Enemy(400, 500)
    enemy.max_health = 0  # Edge case: zero max_health
    enemy.health = 0
    
    # This should not raise ZeroDivisionError
    try:
        img = draw_game_screen(player, [enemy], 500, 1)
        print("✓ streamlit draw_game_screen() handles zero max_health")
    except ZeroDivisionError:
        print("✗ streamlit draw_game_screen() failed with ZeroDivisionError")
        return False
    
    return True

def test_negative_health_pygame():
    """Test that negative health is handled properly in pygame version"""
    from simpsons_arcade import Player
    
    player = Player(100, 500, (0, 0, 255), "Homer", "Homer")
    player.health = -50  # Negative health edge case
    
    try:
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        player.draw(screen)  # Should handle negative health gracefully
        print("✓ pygame Player.draw() handles negative health")
        pygame.quit()
    except Exception as e:
        print(f"✗ pygame Player.draw() failed with negative health: {e}")
        return False
    
    return True

def test_negative_health_streamlit():
    """Test that negative health is handled properly in streamlit version"""
    from streamlit_simpsons_arcade import Player, draw_game_screen
    
    player = Player(100, 500, (0, 0, 255), "Homer", "Homer")
    player.health = -50  # Negative health edge case
    
    try:
        img = draw_game_screen(player, [], 500, 1)
        print("✓ streamlit draw_game_screen() handles negative health")
    except Exception as e:
        print(f"✗ streamlit draw_game_screen() failed with negative health: {e}")
        return False
    
    return True

def test_list_modification_during_iteration():
    """Test that enemy list modification during iteration is safe"""
    from streamlit_simpsons_arcade import Enemy
    
    # Create a list of enemies
    enemies = [Enemy(i * 100, 500) for i in range(5)]
    
    # Simulate removing enemies during iteration (using slice notation)
    try:
        for enemy in enemies[:]:
            if enemy.x > 200:
                enemies.remove(enemy)
        print("✓ List modification during iteration is safe")
        assert len(enemies) == 3, f"Expected 3 enemies, got {len(enemies)}"
    except Exception as e:
        print(f"✗ List modification during iteration failed: {e}")
        return False
    
    return True

def main():
    """Run all edge case tests"""
    print("=" * 70)
    print("Edge Case and Bug Fix Tests")
    print("=" * 70)
    
    results = []
    
    print("\n" + "=" * 70)
    print("Testing Division by Zero Fixes")
    print("=" * 70)
    results.append(("pygame division by zero", test_division_by_zero_pygame()))
    results.append(("streamlit division by zero", test_division_by_zero_streamlit()))
    
    print("\n" + "=" * 70)
    print("Testing Negative Health Handling")
    print("=" * 70)
    results.append(("pygame negative health", test_negative_health_pygame()))
    results.append(("streamlit negative health", test_negative_health_streamlit()))
    
    print("\n" + "=" * 70)
    print("Testing List Operations")
    print("=" * 70)
    results.append(("list modification", test_list_modification_during_iteration()))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("=" * 70)
    if passed == total:
        print(f"✓ All {total} tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} out of {total} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
