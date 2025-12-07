"""
Simple unit tests for the Streamlit version of Simpsons Arcade Game
"""
import sys

# Import the streamlit version classes (they don't depend on streamlit for basic logic)
from streamlit_simpsons_arcade import Character, Player, Enemy, GameState

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
    assert char.attack()  # First attack should succeed
    assert char.is_attacking
    print("✓ Character attack test passed")

def test_collision_detection():
    """Test collision detection"""
    print("Testing collision detection...")
    char1 = Character(100, 100, (255, 0, 0), "Test1")
    
    # Test collision with overlapping rect
    overlapping_rect = (120, 120, 40, 60)
    assert char1.collides_with(overlapping_rect)
    print("✓ Overlapping collision detected")
    
    # Test no collision with distant rect
    distant_rect = (300, 300, 40, 60)
    assert not char1.collides_with(distant_rect)
    print("✓ No collision with distant rect")
    
    print("✓ Collision detection test passed")

def test_game_states():
    """Test game states enum"""
    print("Testing game states...")
    assert GameState.MENU.value == 1
    assert GameState.PLAYING.value == 2
    assert GameState.GAME_OVER.value == 3
    assert GameState.VICTORY.value == 4
    print("✓ Game states test passed")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running Streamlit Simpsons Arcade Tests")
    print("="*50 + "\n")
    
    try:
        test_character_creation()
        test_player_creation()
        test_enemy_creation()
        test_character_movement()
        test_character_attack()
        test_collision_detection()
        test_game_states()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50 + "\n")
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
