# ArcadeClassics
Emulations of classic arcade games

## The Simpsons Arcade Game

A Python recreation of the classic 1991 Konami arcade beat 'em up game "The Simpsons".

**Available in two versions:**
- **Pygame Version**: Traditional desktop game with real-time action
- **Streamlit Version**: Web-based, turn-based gameplay playable in your browser

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

#### Quick Start

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**That's it!** The pygame package includes SDL2 libraries in its pre-built wheels, so no additional system dependencies are needed for most users.

#### Platform-Specific Notes

- **Linux**: Works out of the box with pip-installed pygame
- **macOS**: Works out of the box with pip-installed pygame  
- **Windows**: Works out of the box with pip-installed pygame
- **Streamlit Cloud**: Fully supported (see [Deployment Guide](DEPLOYMENT.md))

#### Troubleshooting SDL Dependencies

If you encounter SDL-related errors (`sdl2-config: not found`), you have two options:

**Option 1: Use pre-built pygame wheels (recommended)**
```bash
pip install --upgrade pip
pip install pygame==2.5.2 --only-binary :all:
```

**Option 2: Install system SDL2 libraries**

Ubuntu/Debian:
```bash
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip install -r requirements.txt
```

macOS (using Homebrew):
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install -r requirements.txt
```

For complete deployment instructions including Streamlit Cloud, Docker, and other platforms, see [DEPLOYMENT.md](DEPLOYMENT.md).

### How to Play

**Option 1: Streamlit Web Version (Recommended for beginners)**

Run the web-based version in your browser:
```bash
streamlit run streamlit_simpsons_arcade.py
```

This will open the game in your default web browser. Features include:
- Interactive web interface with buttons and controls
- Turn-based gameplay
- Difficulty selection (Easy, Normal, Hard)
- Visual game stats and action log
- No pygame/SDL dependencies required for display

**Option 2: Pygame Desktop Version**

Run the traditional desktop game:
```bash
python simpsons_arcade.py
```

### Controls

**Streamlit Version:**
- Click movement buttons (⬅️ ➡️ ⬆️ ⬇️) to move your character
- Click "⚔️ Attack" button to attack enemies
- All interactions via web interface buttons

**Pygame Version:**

- **Arrow Keys**: Move your character (Left/Right/Up/Down)
- **Z**: Attack
- **X**: Jump
- **ESC**: Return to menu / Quit game

### Gameplay

**Streamlit Version:**
1. **Character Selection**: Choose your character using radio buttons
2. **Difficulty**: Select Easy, Normal, or Hard using the slider
3. **Combat**: Click movement buttons to position yourself, then click Attack when enemies are in range
4. **Turn-based**: Each action you take triggers enemy responses
5. **Progress**: Defeat all enemies in each level to advance
6. **Score**: Earn 100 points for each enemy defeated
7. **Win Condition**: Complete all 3 levels to achieve victory

**Pygame Version:**

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

**Streamlit Version:**
- Built with Python and Streamlit
- Turn-based gameplay mechanics
- PIL/Pillow for game rendering
- Session state for game persistence
- Web-based interface with responsive layout
- No browser-specific requirements (works on all modern browsers)

**Pygame Version:**

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

### Browser Compatibility (Streamlit Version)

The Streamlit version works on all modern web browsers:
- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (responsive layout)

**System Requirements:**
- Python 3.7 or higher
- Modern web browser with JavaScript enabled
- Internet connection (for initial Streamlit download)

**Troubleshooting:**
- If the game doesn't load, ensure you have the latest dependencies: `pip install -r requirements.txt --upgrade`
- For slower connections, the initial load may take a few seconds
- If buttons don't respond, try refreshing the browser page
- Clear browser cache if you experience display issues

Enjoy playing The Simpsons Arcade Game!
