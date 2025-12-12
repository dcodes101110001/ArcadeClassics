"""
The Simpsons Arcade Game - Streamlit Edition
A web-based version of the classic 1991 arcade game, playable in your browser.
"""

import streamlit as st
import random
from enum import Enum
from PIL import Image, ImageDraw
import io

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
SKY_BLUE = (135, 206, 235)

# Game States
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    VICTORY = 4

# Character Classes
class Character:
    """Base class for game characters"""
    def __init__(self, x, y, color, name, attack_power=10, health=100):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.color = color
        self.name = name
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.speed = 5
        self.facing_right = True
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_range = 60
        
    def move(self, dx, dy):
        """Move the character"""
        self.x += dx
        self.y += dy
        
        # Keep character on screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height - 100))
    
    def attack(self):
        """Perform attack"""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 3  # Reduced for turn-based gameplay
            return True
        return False
    
    def update(self):
        """Update character state"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_cooldown == 0:
            self.is_attacking = False
    
    def get_attack_rect(self):
        """Get the attack hitbox"""
        if self.facing_right:
            return (self.x + self.width, self.y + 20, self.attack_range, 20)
        else:
            return (self.x - self.attack_range, self.y + 20, self.attack_range, 20)
    
    def get_rect(self):
        """Get character collision rect"""
        return (self.x, self.y, self.width, self.height)
    
    def collides_with(self, other_rect):
        """Check collision with another rect (x, y, width, height)"""
        x1, y1, w1, h1 = self.get_rect()
        x2, y2, w2, h2 = other_rect
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

class Player(Character):
    """Player character"""
    def __init__(self, x, y, color, name, character_type):
        super().__init__(x, y, color, name)
        self.character_type = character_type
        self.score = 0
        
        # Set character-specific attributes
        if character_type == "Homer":
            self.attack_power = 15
            self.speed = 4
            self.max_health = 120
        elif character_type == "Marge":
            self.attack_power = 12
            self.speed = 5
            self.max_health = 100
        elif character_type == "Bart":
            self.attack_power = 10
            self.speed = 6
            self.max_health = 90
        elif character_type == "Lisa":
            self.attack_power = 11
            self.speed = 5
            self.max_health = 95
        
        self.health = self.max_health

class Enemy(Character):
    """Enemy character"""
    def __init__(self, x, y):
        color = random.choice([PURPLE, GRAY, ORANGE])
        super().__init__(x, y, color, "Enemy", attack_power=8, health=30)
        
    def ai_action(self, player, damage_multiplier=1.0):
        """Simple AI behavior for turn-based gameplay"""
        # Calculate distance to player
        dx = player.x - self.x
        distance = abs(dx)
        
        # Attack if close enough
        if distance < 80:
            if self.attack():
                attack_rect = self.get_attack_rect()
                if player.collides_with(attack_rect):
                    damage = int(self.attack_power * damage_multiplier)
                    player.health -= damage
                    return f"Enemy attacked {player.name} for {damage} damage!"
            return "Enemy preparing to attack..."
        
        # Move towards player
        elif dx > 0:
            self.move(min(3, dx), 0)
            self.facing_right = True
            return "Enemy moves closer..."
        else:
            self.move(max(-3, dx), 0)
            self.facing_right = False
            return "Enemy moves closer..."

def draw_game_screen(player, enemies, ground_level, level):
    """Draw the game screen using PIL"""
    # Create image
    img = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), SKY_BLUE)
    draw = ImageDraw.Draw(img)
    
    # Draw ground
    draw.rectangle([(0, ground_level + 60), (SCREEN_WIDTH, SCREEN_HEIGHT)], fill=GREEN)
    
    # Draw player
    if player:
        # Draw body
        draw.rectangle([(player.x, player.y), 
                       (player.x + player.width, player.y + player.height)], 
                      fill=player.color, outline=BLACK)
        
        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = player.health / player.max_health if player.max_health > 0 else 0
        draw.rectangle([(player.x, player.y - 10), 
                       (player.x + health_bar_width, player.y - 10 + health_bar_height)], 
                      fill=RED)
        draw.rectangle([(player.x, player.y - 10), 
                       (player.x + health_bar_width * health_percentage, player.y - 10 + health_bar_height)], 
                      fill=GREEN)
        
        # Draw attack indicator
        if player.is_attacking:
            attack_x = player.x + player.width if player.facing_right else player.x - player.attack_range
            draw.rectangle([(attack_x, player.y + 20), 
                          (attack_x + player.attack_range, player.y + 40)], 
                         outline=YELLOW, width=2)
    
    # Draw enemies
    for enemy in enemies:
        # Draw body
        draw.rectangle([(enemy.x, enemy.y), 
                       (enemy.x + enemy.width, enemy.y + enemy.height)], 
                      fill=enemy.color, outline=BLACK)
        
        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = enemy.health / enemy.max_health if enemy.max_health > 0 else 0
        draw.rectangle([(enemy.x, enemy.y - 10), 
                       (enemy.x + health_bar_width, enemy.y - 10 + health_bar_height)], 
                      fill=RED)
        draw.rectangle([(enemy.x, enemy.y - 10), 
                       (enemy.x + health_bar_width * health_percentage, enemy.y - 10 + health_bar_height)], 
                      fill=GREEN)
        
        # Draw attack indicator
        if enemy.is_attacking:
            attack_x = enemy.x + enemy.width if enemy.facing_right else enemy.x - enemy.attack_range
            draw.rectangle([(attack_x, enemy.y + 20), 
                          (attack_x + enemy.attack_range, enemy.y + 40)], 
                         outline=YELLOW, width=2)
    
    return img

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = GameState.MENU
    if 'player' not in st.session_state:
        st.session_state.player = None
    if 'enemies' not in st.session_state:
        st.session_state.enemies = []
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'ground_level' not in st.session_state:
        st.session_state.ground_level = SCREEN_HEIGHT - 100
    if 'selected_character' not in st.session_state:
        st.session_state.selected_character = "Homer"
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = "Normal"
    if 'action_log' not in st.session_state:
        st.session_state.action_log = []

def reset_game():
    """Reset game state"""
    character_name = st.session_state.selected_character
    colors = {"Homer": BLUE, "Marge": GREEN, "Bart": YELLOW, "Lisa": RED}
    
    st.session_state.player = Player(100, st.session_state.ground_level, 
                                     colors[character_name], character_name, character_name)
    st.session_state.enemies = []
    st.session_state.level = 1
    st.session_state.action_log = ["Game started!"]
    
    # Adjust difficulty
    enemy_count = 3
    if st.session_state.difficulty == "Easy":
        enemy_count = 2
    elif st.session_state.difficulty == "Hard":
        enemy_count = 4
    
    spawn_enemies(enemy_count)

def spawn_enemies(count):
    """Spawn enemies"""
    for i in range(count):
        x = random.randint(400, SCREEN_WIDTH - 100)
        enemy = Enemy(x, st.session_state.ground_level)
        st.session_state.enemies.append(enemy)

def add_to_log(message):
    """Add message to action log"""
    st.session_state.action_log.append(message)
    if len(st.session_state.action_log) > 10:
        st.session_state.action_log.pop(0)

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="The Simpsons Arcade Game",
        page_icon="🎯",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Title
    st.title("🎮 The Simpsons Arcade Game")
    st.markdown("*A web-based recreation of the classic 1991 arcade game*")
    
    # Main game logic based on state
    if st.session_state.game_state == GameState.MENU:
        show_menu()
    elif st.session_state.game_state == GameState.PLAYING:
        show_game()
    elif st.session_state.game_state == GameState.GAME_OVER:
        show_game_over()
    elif st.session_state.game_state == GameState.VICTORY:
        show_victory()

def show_menu():
    """Show the main menu"""
    st.header("Main Menu")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Character Selection")
        
        # Character descriptions
        character_info = {
            "Homer": {"emoji": "🍩", "desc": "High attack, slow speed, most health (Tank)", 
                     "attack": 15, "speed": 4, "health": 120},
            "Marge": {"emoji": "💙", "desc": "Balanced stats, good all-rounder", 
                     "attack": 12, "speed": 5, "health": 100},
            "Bart": {"emoji": "🛹", "desc": "Fast movement, lower health (Speed)", 
                    "attack": 10, "speed": 6, "health": 90},
            "Lisa": {"emoji": "🎷", "desc": "Balanced speed and attack", 
                    "attack": 11, "speed": 5, "health": 95}
        }
        
        st.session_state.selected_character = st.radio(
            "Choose your character:",
            ["Homer", "Marge", "Bart", "Lisa"],
            format_func=lambda x: f"{character_info[x]['emoji']} {x} - {character_info[x]['desc']}"
        )
        
        # Show character stats
        char = character_info[st.session_state.selected_character]
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Attack Power", char['attack'])
        col_b.metric("Speed", char['speed'])
        col_c.metric("Max Health", char['health'])
        
        st.subheader("Difficulty")
        st.session_state.difficulty = st.select_slider(
            "Select difficulty level:",
            options=["Easy", "Normal", "Hard"],
            value=st.session_state.difficulty
        )
        
        if st.session_state.difficulty == "Easy":
            st.info("🟢 Easy: 2 enemies per level, enemies deal less damage")
        elif st.session_state.difficulty == "Normal":
            st.info("🟡 Normal: 3 enemies per level, standard gameplay")
        else:
            st.info("🔴 Hard: 4 enemies per level, enemies deal more damage")
    
    with col2:
        st.subheader("How to Play")
        st.markdown("""
        **Controls:**
        - Use movement buttons to navigate
        - Click 'Attack' to fight enemies
        - Defeat all enemies to advance
        
        **Objective:**
        - Complete 3 levels to win
        - Earn points by defeating enemies
        - Manage your health wisely
        
        **Tips:**
        - Keep your distance from enemies
        - Attack when they're in range
        - Each character has unique strengths
        """)
    
    st.markdown("---")
    if st.button("🎮 Start Game", type="primary", use_container_width=True):
        reset_game()
        st.session_state.game_state = GameState.PLAYING
        st.rerun()

def show_game():
    """Show the game screen"""
    player = st.session_state.player
    enemies = st.session_state.enemies
    
    # Check win/lose conditions
    if player.health <= 0:
        st.session_state.game_state = GameState.GAME_OVER
        st.rerun()
    
    if len(enemies) == 0:
        st.session_state.level += 1
        if st.session_state.level > 3:
            st.session_state.game_state = GameState.VICTORY
            st.rerun()
        else:
            add_to_log(f"Level {st.session_state.level - 1} complete! Starting Level {st.session_state.level}")
            player.health = min(player.health + 30, player.max_health)
            
            enemy_count = 3
            if st.session_state.difficulty == "Easy":
                enemy_count = 2
            elif st.session_state.difficulty == "Hard":
                enemy_count = 4
            
            spawn_enemies(enemy_count + st.session_state.level - 1)
    
    # Layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Draw game screen
        img = draw_game_screen(player, enemies, st.session_state.ground_level, st.session_state.level)
        st.image(img, use_container_width=True)
        
        # Controls
        st.subheader("Controls")
        control_cols = st.columns(5)
        
        with control_cols[0]:
            if st.button("⬅️ Left", use_container_width=True):
                player.move(-player.speed * 3, 0)
                player.facing_right = False
                add_to_log(f"{player.name} moves left")
                enemy_actions()
                st.rerun()
        
        with control_cols[1]:
            if st.button("➡️ Right", use_container_width=True):
                player.move(player.speed * 3, 0)
                player.facing_right = True
                add_to_log(f"{player.name} moves right")
                enemy_actions()
                st.rerun()
        
        with control_cols[2]:
            if st.button("⬆️ Up", use_container_width=True):
                player.move(0, -player.speed * 3)
                add_to_log(f"{player.name} moves up")
                enemy_actions()
                st.rerun()
        
        with control_cols[3]:
            if st.button("⬇️ Down", use_container_width=True):
                player.move(0, player.speed * 3)
                add_to_log(f"{player.name} moves down")
                enemy_actions()
                st.rerun()
        
        with control_cols[4]:
            attack_disabled = player.attack_cooldown > 0
            if st.button("⚔️ Attack", type="primary", use_container_width=True, disabled=attack_disabled):
                if player.attack():
                    attack_rect = player.get_attack_rect()
                    hit_any = False
                    for enemy in enemies[:]:
                        if enemy.collides_with(attack_rect):
                            enemy.health -= player.attack_power
                            add_to_log(f"{player.name} attacks enemy for {player.attack_power} damage!")
                            if enemy.health <= 0:
                                enemies.remove(enemy)
                                player.score += 100
                                add_to_log(f"Enemy defeated! +100 points")
                            hit_any = True
                    
                    if not hit_any:
                        add_to_log(f"{player.name} attacks but misses!")
                    
                    enemy_actions()
                    st.rerun()
    
    with col2:
        st.subheader("Game Stats")
        
        st.metric("Character", player.character_type)
        st.metric("Level", st.session_state.level)
        st.metric("Score", player.score)
        
        # Health bar
        st.markdown("**Health**")
        health_percentage = max(0, player.health / player.max_health) if player.max_health > 0 else 0
        st.progress(health_percentage)
        st.text(f"{max(0, player.health)}/{player.max_health}")
        
        st.metric("Enemies Remaining", len(enemies))
        
        if player.attack_cooldown > 0:
            st.warning(f"⏳ Attack cooldown: {player.attack_cooldown}")
        
        st.markdown("---")
        st.subheader("Action Log")
        for log_entry in reversed(st.session_state.action_log[-5:]):
            st.text(f"• {log_entry}")
        
        st.markdown("---")
        if st.button("🚪 Return to Menu", use_container_width=True):
            st.session_state.game_state = GameState.MENU
            st.rerun()

def enemy_actions():
    """Execute enemy AI actions"""
    player = st.session_state.player
    
    # Apply difficulty modifier
    damage_multiplier = 1.0
    if st.session_state.difficulty == "Easy":
        damage_multiplier = 0.7
    elif st.session_state.difficulty == "Hard":
        damage_multiplier = 1.3
    
    for enemy in st.session_state.enemies:
        enemy.update()
        message = enemy.ai_action(player, damage_multiplier)
        if message:
            add_to_log(message)
    
    # Update player
    player.update()

def show_game_over():
    """Show game over screen"""
    st.header("💀 Game Over")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.error("You were defeated!")
        
        if st.session_state.player:
            st.metric("Final Score", st.session_state.player.score)
            st.metric("Level Reached", st.session_state.level)
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Play Again", type="primary", use_container_width=True):
                reset_game()
                st.session_state.game_state = GameState.PLAYING
                st.rerun()
        
        with col_b:
            if st.button("🏠 Main Menu", use_container_width=True):
                st.session_state.game_state = GameState.MENU
                st.rerun()

def show_victory():
    """Show victory screen"""
    st.header("🏆 Victory!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.success("You defeated all enemies and completed all levels!")
        st.balloons()
        
        if st.session_state.player:
            st.metric("Final Score", st.session_state.player.score)
            st.metric("Difficulty", st.session_state.difficulty)
            st.metric("Character", st.session_state.player.character_type)
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 Play Again", type="primary", use_container_width=True):
                reset_game()
                st.session_state.game_state = GameState.PLAYING
                st.rerun()
        
        with col_b:
            if st.button("🏠 Main Menu", use_container_width=True):
                st.session_state.game_state = GameState.MENU
                st.rerun()

if __name__ == "__main__":
    main()
