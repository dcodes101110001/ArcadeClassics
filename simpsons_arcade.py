"""
The Simpsons Arcade Game
A side-scrolling beat 'em up game inspired by the classic 1991 arcade game.
"""

import pygame
import sys
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

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
        self.jump_power = 15
        self.velocity_y = 0
        self.is_jumping = False
        self.facing_right = True
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_range = 60
        
    def draw(self, screen):
        """Draw the character"""
        # Draw body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw health bar
        health_bar_width = 40
        health_bar_height = 5
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, health_bar_width * health_percentage, health_bar_height))
        
        # Draw attack indicator
        if self.is_attacking:
            attack_x = self.x + self.width if self.facing_right else self.x - self.attack_range
            pygame.draw.rect(screen, YELLOW, (attack_x, self.y + 20, self.attack_range, 20), 2)
    
    def move(self, dx, dy):
        """Move the character"""
        self.x += dx
        self.y += dy
        
        # Keep character on screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        
    def jump(self):
        """Make the character jump"""
        if not self.is_jumping:
            self.velocity_y = -self.jump_power
            self.is_jumping = True
    
    def apply_gravity(self, ground_level):
        """Apply gravity to the character"""
        self.velocity_y += 0.8
        self.y += self.velocity_y
        
        # Check if landed on ground
        if self.y >= ground_level:
            self.y = ground_level
            self.velocity_y = 0
            self.is_jumping = False
    
    def attack(self):
        """Perform attack"""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 20
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
            return pygame.Rect(self.x + self.width, self.y + 20, self.attack_range, 20)
        else:
            return pygame.Rect(self.x - self.attack_range, self.y + 20, self.attack_range, 20)
    
    def get_rect(self):
        """Get character collision rect"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

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
        self.ai_timer = 0
        self.ai_state = "chase"
        self.direction = random.choice([-1, 1])
        
    def ai_update(self, player, ground_level):
        """Simple AI behavior"""
        self.ai_timer += 1
        
        # Calculate distance to player
        dx = player.x - self.x
        distance = abs(dx)
        
        # Chase player if far away
        if distance > 150:
            if dx > 0:
                self.move(2, 0)
                self.facing_right = True
            else:
                self.move(-2, 0)
                self.facing_right = False
        
        # Attack if close enough
        elif distance < 80:
            if self.attack_cooldown <= 0:
                self.attack()
                # Check if attack hits player
                if self.is_attacking:
                    attack_rect = self.get_attack_rect()
                    player_rect = player.get_rect()
                    if attack_rect.colliderect(player_rect):
                        player.health -= self.attack_power
        
        # Random movement
        elif self.ai_timer % 60 == 0:
            self.direction = random.choice([-1, 1])
            
        if self.ai_timer % 120 == 0 and random.random() < 0.3:
            self.jump()
        
        # Apply gravity
        self.apply_gravity(ground_level)

class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Simpsons Arcade Game")
        self.clock = pygame.time.Clock()
        self.state = GameState.MENU
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.player = None
        self.enemies = []
        self.ground_level = SCREEN_HEIGHT - 100
        self.level = 1
        self.enemies_defeated = 0
        self.selected_character = 0
        self.characters = ["Homer", "Marge", "Bart", "Lisa"]
        
    def reset_game(self):
        """Reset game state"""
        character_name = self.characters[self.selected_character]
        colors = {"Homer": BLUE, "Marge": GREEN, "Bart": YELLOW, "Lisa": RED}
        
        self.player = Player(100, self.ground_level, colors[character_name], character_name, character_name)
        self.enemies = []
        self.level = 1
        self.enemies_defeated = 0
        self.spawn_enemies(3)
        
    def spawn_enemies(self, count):
        """Spawn enemies"""
        for i in range(count):
            x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 500)
            enemy = Enemy(x, self.ground_level)
            self.enemies.append(enemy)
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font.render("THE SIMPSONS ARCADE GAME", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Character selection
        select_text = self.small_font.render("Select Character (Arrow Keys):", True, WHITE)
        select_rect = select_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(select_text, select_rect)
        
        # Character options
        for i, char in enumerate(self.characters):
            color = WHITE if i == self.selected_character else GRAY
            char_text = self.font.render(char, True, color)
            char_rect = char_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            self.screen.blit(char_text, char_rect)
        
        # Instructions
        start_text = self.small_font.render("Press SPACE to Start", True, GREEN)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(start_text, start_rect)
        
        # Controls
        controls = [
            "Controls:",
            "Arrow Keys - Move",
            "Z - Attack",
            "X - Jump",
            "ESC - Quit"
        ]
        y_offset = 300
        for text in controls:
            control_text = self.small_font.render(text, True, WHITE)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(control_text, control_rect)
            y_offset += 25
    
    def draw_game(self):
        """Draw game screen"""
        self.screen.fill((135, 206, 235))  # Sky blue
        
        # Draw ground
        pygame.draw.rect(self.screen, GREEN, (0, self.ground_level + 60, SCREEN_WIDTH, 40))
        
        # Draw player
        if self.player:
            self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw HUD
        if self.player:
            # Score
            score_text = self.small_font.render(f"Score: {self.player.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            # Level
            level_text = self.small_font.render(f"Level: {self.level}", True, BLACK)
            self.screen.blit(level_text, (10, 40))
            
            # Enemies remaining
            enemies_text = self.small_font.render(f"Enemies: {len(self.enemies)}", True, BLACK)
            self.screen.blit(enemies_text, (10, 70))
            
            # Character name
            char_text = self.small_font.render(f"Character: {self.player.character_type}", True, BLACK)
            self.screen.blit(char_text, (SCREEN_WIDTH - 200, 10))
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        if self.player:
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(score_text, score_rect)
        
        restart_text = self.small_font.render("Press SPACE to Return to Menu", True, GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_victory(self):
        """Draw victory screen"""
        self.screen.fill(BLACK)
        
        victory_text = self.font.render("VICTORY!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(victory_text, victory_rect)
        
        if self.player:
            score_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(score_text, score_rect)
        
        continue_text = self.small_font.render("Press SPACE to Return to Menu", True, GREEN)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(continue_text, continue_rect)
    
    def handle_menu_input(self):
        """Handle menu input"""
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_UP:
                    self.selected_character = (self.selected_character - 1) % len(self.characters)
                elif event.key == pygame.K_DOWN:
                    self.selected_character = (self.selected_character + 1) % len(self.characters)
                elif event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = GameState.PLAYING
        
        return True
    
    def handle_game_input(self):
        """Handle game input"""
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
                    return True
                
                if event.key == pygame.K_z:
                    if self.player.attack():
                        # Check for hits on enemies
                        attack_rect = self.player.get_attack_rect()
                        for enemy in self.enemies[:]:
                            if attack_rect.colliderect(enemy.get_rect()):
                                enemy.health -= self.player.attack_power
                                if enemy.health <= 0:
                                    self.enemies.remove(enemy)
                                    self.player.score += 100
                                    self.enemies_defeated += 1
                
                if event.key == pygame.K_x:
                    self.player.jump()
        
        # Movement
        if keys[pygame.K_LEFT]:
            self.player.move(-self.player.speed, 0)
            self.player.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.player.move(self.player.speed, 0)
            self.player.facing_right = True
        if keys[pygame.K_UP]:
            self.player.move(0, -self.player.speed)
        if keys[pygame.K_DOWN]:
            self.player.move(0, self.player.speed)
        
        # Keep player above ground
        if self.player.y > self.ground_level:
            self.player.y = self.ground_level
        
        return True
    
    def handle_game_over_input(self):
        """Handle game over input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = GameState.MENU
                if event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update_game(self):
        """Update game state"""
        if not self.player:
            return
        
        # Update player
        self.player.update()
        self.player.apply_gravity(self.ground_level)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update()
            enemy.ai_update(self.player, self.ground_level)
        
        # Check if player is dead
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER
        
        # Check if level is complete
        if len(self.enemies) == 0:
            self.level += 1
            if self.level > 3:  # Win after 3 levels
                self.state = GameState.VICTORY
            else:
                # Spawn more enemies for next level
                self.spawn_enemies(3 + self.level)
                self.player.health = min(self.player.health + 30, self.player.max_health)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            if self.state == GameState.MENU:
                running = self.handle_menu_input()
                self.draw_menu()
            
            elif self.state == GameState.PLAYING:
                running = self.handle_game_input()
                self.update_game()
                self.draw_game()
            
            elif self.state == GameState.GAME_OVER:
                running = self.handle_game_over_input()
                self.draw_game_over()
            
            elif self.state == GameState.VICTORY:
                running = self.handle_game_over_input()
                self.draw_victory()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
