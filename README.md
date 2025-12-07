# ArcadeClassics
Emulations of classic arcade games

## The Simpsons Arcade Game

A Python/Pygame recreation of the classic 1991 Konami arcade beat 'em up game "The Simpsons".

### Features

- **Four Playable Characters**: Choose from Homer, Marge, Bart, or Lisa, each with unique stats
  - **Homer**: High attack power, slower movement, most health (Tank)
  - **Marge**: Balanced stats, good all-rounder
  - **Bart**: Fast movement, lower health, quick attacks (Speed)
  - **Lisa**: Balanced speed and attack, moderate health

- **Side-scrolling Beat 'em Up Gameplay**: Classic arcade action
- **Multiple Levels**: Progress through increasingly difficult waves of enemies
- **Combat System**: Attack enemies with simple but satisfying combat mechanics
- **Score System**: Earn points by defeating enemies
- **Health Management**: Each character has health that can be depleted by enemy attacks

### Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### How to Play

Run the game:
```bash
python simpsons_arcade.py
```

### Controls

- **Arrow Keys**: Move your character (Left/Right/Up/Down)
- **Z**: Attack
- **X**: Jump
- **ESC**: Return to menu / Quit game

### Gameplay

1. **Character Selection**: Use Up/Down arrow keys to select your character, press SPACE to start
2. **Combat**: Use the Z key to attack enemies when they're in range
3. **Movement**: Navigate using arrow keys to dodge enemy attacks
4. **Jump**: Press X to jump over obstacles or avoid attacks
5. **Survive**: Defeat all enemies in each level to progress
6. **Score**: Earn 100 points for each enemy defeated

### Game Objectives

- Defeat all enemies in each level
- Complete 3 levels to achieve victory
- Try to get the highest score possible!

### Tips

- Keep moving to avoid enemy attacks
- Time your attacks carefully - there's a cooldown between attacks
- Each character has different strengths - experiment to find your favorite!
- Homer is great for beginners with his high health
- Bart is excellent for experienced players who can dodge effectively

### Technical Details

- Built with Python and Pygame
- 60 FPS gameplay
- Simple sprite-based graphics
- Basic AI for enemy behavior
- Collision detection for combat

### Future Enhancements

Potential features for future versions:
- More detailed sprite graphics
- Additional levels and level variety
- Power-ups and collectibles
- Boss battles
- Co-op multiplayer support
- Sound effects and music
- Special combo moves
- Different enemy types

Enjoy playing The Simpsons Arcade Game!
