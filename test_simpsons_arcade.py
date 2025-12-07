"""
Simple unit tests for the Simpsons Arcade Game
"""
import sys
import os

# Set headless mode for testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from simpsons_arcade import Character, Player, Enemy, Game, GameState

def test_character_creation():
    """Test character creation"""
    print("Testing character creation...")
    char = Character(100, 100, (255, 0, 0), "Test", attack_power=10, health=100)
    assert char.x == 100
    assert char.y == 100
    assert char.health == 100
    assert char.attack_power == 10
    print("✓ Character creation test passed")

def test_player_creation():
    """Test player character creation"""
    print("Testing player creation...")
    
    # Test Homer
    homer = Player(100, 100, (0, 0, 255), "Homer", "Homer")
    assert homer.character_type == "Homer"
    assert homer.attack_power == 15
    assert homer.max_health == 120
    print("✓ Homer created correctly")
    
    # Test Bart
    bart = Player(100, 100, (255, 255, 0), "Bart", "Bart")
    assert bart.character_type == "Bart"
    assert bart.speed == 6
    assert bart.max_health == 90
    print("✓ Bart created correctly")
    
    print("✓ Player creation test passed")

def test_enemy_creation():
    """Test enemy creation"""
    print("Testing enemy creation...")
    enemy = Enemy(200, 100)
    assert enemy.name == "Enemy"
    assert enemy.health == 30
    assert enemy.attack_power == 8
    print("✓ Enemy creation test passed")

def test_character_movement():
    """Test character movement"""
    print("Testing character movement...")
    char = Character(100, 100, (255, 0, 0), "Test")
    original_x = char.x
    char.move(10, 0)
    assert char.x == original_x + 10
    print("✓ Character movement test passed")

def test_character_attack():
    """Test character attack"""
    print("Testing character attack...")
    char = Character(100, 100, (255, 0, 0), "Test")
    assert char.attack() == True  # First attack should succeed
    assert char.is_attacking == True
    print("✓ Character attack test passed")

def test_game_initialization():
    """Test game initialization"""
    print("Testing game initialization...")
    pygame.init()
    game = Game()
    assert game.state == GameState.MENU
    assert game.level == 1
    assert len(game.characters) == 4
    assert "Homer" in game.characters
    assert "Marge" in game.characters
    assert "Bart" in game.characters
    assert "Lisa" in game.characters
    print("✓ Game initialization test passed")

def test_game_reset():
    """Test game reset"""
    print("Testing game reset...")
    pygame.init()
    game = Game()
    game.reset_game()
    assert game.player is not None
    assert game.level == 1
    assert len(game.enemies) > 0
    print("✓ Game reset test passed")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running Simpsons Arcade Game Tests")
    print("="*50 + "\n")
    
    try:
        test_character_creation()
        test_player_creation()
        test_enemy_creation()
        test_character_movement()
        test_character_attack()
        test_game_initialization()
        test_game_reset()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
