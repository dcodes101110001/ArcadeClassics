# Deployment Guide for The Simpsons Arcade Game

This guide provides detailed instructions for deploying and running The Simpsons Arcade Game across different platforms and environments.

## Table of Contents
- [Local Installation](#local-installation)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Troubleshooting](#troubleshooting)
- [Dependencies Overview](#dependencies-overview)

## Local Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/dcodes101110001/ArcadeClassics.git
   cd ArcadeClassics
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   
   For the Streamlit web version (recommended):
   ```bash
   streamlit run streamlit_simpsons_arcade.py
   ```
   
   For the pygame desktop version:
   ```bash
   python simpsons_arcade.py
   ```

## Streamlit Cloud Deployment

Streamlit Cloud is a free platform for hosting Streamlit apps. This game works perfectly on Streamlit Cloud!

### Setup Steps

1. **Fork/Push the repository to GitHub**
   - Ensure the repository is in your GitHub account

2. **Sign in to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy the app**
   - Click "New app"
   - Select your repository: `dcodes101110001/ArcadeClassics`
   - Main file path: `streamlit_simpsons_arcade.py`
   - Click "Deploy"

### Required Files for Streamlit Cloud

The repository includes two critical files for Streamlit Cloud deployment:

1. **`requirements.txt`** - Python dependencies
   - Contains pygame, streamlit, and Pillow
   - pygame includes pre-built SDL2 binaries for Linux

2. **`packages.txt`** - System dependencies (apt packages)
   - Contains SDL2 development libraries
   - Required if pygame needs to build from source
   - Auto-installed by Streamlit Cloud

### Why packages.txt is Important

Streamlit Cloud runs on Linux (Debian/Ubuntu). While pygame's pre-built wheels include SDL2 binaries, some scenarios require system SDL2 libraries:
- Building pygame from source (if wheel not available)
- Certain pygame features requiring system libraries
- Fallback for compatibility

The `packages.txt` file ensures SDL2 libraries are available:
```
libsdl2-dev
libsdl2-image-dev
libsdl2-mixer-dev
libsdl2-ttf-dev
libfreetype6-dev
libportmidi-dev
```

## Platform-Specific Instructions

### Linux (Ubuntu/Debian)

**For Streamlit version only:**
```bash
pip install -r requirements.txt
streamlit run streamlit_simpsons_arcade.py
```

**For pygame desktop version:**
```bash
# Install system SDL2 libraries (if not using pre-built pygame wheels)
sudo apt-get update
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python simpsons_arcade.py
```

### Linux (Fedora/RHEL/CentOS)

```bash
# Install system SDL2 libraries
sudo dnf install -y \
    SDL2-devel \
    SDL2_image-devel \
    SDL2_mixer-devel \
    SDL2_ttf-devel \
    freetype-devel \
    portmidi-devel

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python simpsons_arcade.py  # or streamlit run streamlit_simpsons_arcade.py
```

### macOS

**Using Homebrew (recommended):**
```bash
# Install Homebrew if not already installed
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install SDL2 libraries (optional - pygame wheels include SDL2)
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python simpsons_arcade.py  # or streamlit run streamlit_simpsons_arcade.py
```

### Windows

**Easiest method (using pre-built wheels):**
```bash
# Install Python dependencies (pygame wheels include SDL2 DLLs)
pip install -r requirements.txt

# Run the game
python simpsons_arcade.py  # or streamlit run streamlit_simpsons_arcade.py
```

**If building from source is needed:**
1. Download SDL2 development libraries from [libsdl.org](https://www.libsdl.org/download-2.0.php)
2. Extract to a location (e.g., `C:\SDL2`)
3. Set environment variables:
   ```
   set SDL2_DIR=C:\SDL2
   ```
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Troubleshooting

### Error: "sdl2-config: not found"

This error occurs when pygame tries to build from source but can't find SDL2 system libraries.

**Solutions:**

1. **Preferred: Use pre-built pygame wheels**
   ```bash
   pip install --upgrade pip
   pip install pygame==2.5.2 --only-binary :all:
   ```

2. **Install system SDL2 libraries**
   
   Ubuntu/Debian:
   ```bash
   sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   ```
   
   macOS:
   ```bash
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
   ```

3. **For Streamlit Cloud:**
   - Ensure `packages.txt` is in the repository root
   - Contains the SDL2 library names (already configured)

### Error: "No module named 'pygame'"

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Error: "streamlit: command not found"

```bash
pip install --upgrade streamlit
```

### Pygame window doesn't appear (headless environments)

For testing in headless environments (CI/CD, servers):
```bash
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
python simpsons_arcade.py
```

Or for the Streamlit version (which doesn't require display):
```bash
streamlit run streamlit_simpsons_arcade.py --server.headless true
```

### Performance issues on Streamlit Cloud

- Streamlit Cloud free tier has resource limitations
- The game should run smoothly on the free tier
- If experiencing slowness:
  - Clear browser cache
  - Try a different browser
  - Check Streamlit Cloud status

## Dependencies Overview

### Python Dependencies (requirements.txt)

| Package | Version | Purpose | SDL Requirement |
|---------|---------|---------|-----------------|
| pygame | 2.5.2 | Desktop game engine | Includes SDL2 in wheels |
| streamlit | >=1.28.0 | Web interface | Not required |
| Pillow | >=10.0.0 | Image rendering | Not required |

### System Dependencies (packages.txt)

These are Linux packages installed via `apt-get` on Streamlit Cloud:

| Package | Purpose |
|---------|---------|
| libsdl2-dev | SDL2 core library (graphics, input, audio) |
| libsdl2-image-dev | SDL2 image loading (PNG, JPG, etc.) |
| libsdl2-mixer-dev | SDL2 audio mixing |
| libsdl2-ttf-dev | SDL2 TrueType font rendering |
| libfreetype6-dev | Font rendering library |
| libportmidi-dev | MIDI support for pygame |

### Understanding pygame and SDL2

**pygame** is a Python wrapper around SDL2 (Simple DirectMedia Layer):
- SDL2 handles low-level graphics, audio, and input
- pygame provides Python-friendly APIs

**Pre-built wheels vs Building from source:**
- **Pre-built wheels** (recommended): Include SDL2 binaries, no system libraries needed
- **Building from source**: Requires system SDL2 development libraries

**When are system SDL2 libraries needed?**
- Building pygame from source (no wheel available for your platform)
- Some advanced pygame features
- Fallback/compatibility on certain systems
- **Good practice**: Install them anyway for maximum compatibility

## Running Tests

```bash
# Run pygame version tests
python test_simpsons_arcade.py

# Run Streamlit version tests
python test_streamlit_simpsons.py
```

Tests use headless mode (SDL dummy drivers) automatically.

## Docker Deployment (Optional)

If you want to containerize the application:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_simpsons_arcade.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t simpsons-arcade .
docker run -p 8501:8501 simpsons-arcade
```

## Cloud Platform Alternatives

### Heroku

Create `Procfile`:
```
web: streamlit run streamlit_simpsons_arcade.py --server.port $PORT --server.address 0.0.0.0
```

Create `Aptfile`:
```
libsdl2-dev
libsdl2-image-dev
libsdl2-mixer-dev
libsdl2-ttf-dev
```

### Railway.app

Works out of the box! Just:
1. Connect your GitHub repository
2. Set start command: `streamlit run streamlit_simpsons_arcade.py`
3. Deploy

### Replit

1. Import from GitHub
2. Set run command: `streamlit run streamlit_simpsons_arcade.py`
3. Replit automatically installs dependencies

## Best Practices

1. **Use pre-built wheels when possible**
   - Faster installation
   - More reliable
   - No compilation required

2. **Keep packages.txt for compatibility**
   - Ensures system libraries available
   - Fallback for platforms without wheels
   - Required for some cloud platforms

3. **Pin pygame version**
   - Ensures consistent behavior
   - `pygame==2.5.2` in requirements.txt

4. **Test locally before deploying**
   - Run `pip install -r requirements.txt`
   - Test both versions of the game

5. **Use virtual environments**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## Support and Resources

- **Streamlit Documentation**: https://docs.streamlit.io
- **Pygame Documentation**: https://www.pygame.org/docs/
- **SDL2 Documentation**: https://wiki.libsdl.org/
- **Python Packaging**: https://packaging.python.org/

## Version Compatibility

Tested and working on:
- ✅ Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Ubuntu 20.04, 22.04, 24.04
- ✅ macOS 12+
- ✅ Windows 10, 11
- ✅ Streamlit Cloud
- ✅ Docker containers

## Summary

**For most users:**
```bash
pip install -r requirements.txt
streamlit run streamlit_simpsons_arcade.py
```

**For Streamlit Cloud:**
- Just deploy - `packages.txt` and `requirements.txt` handle everything

**For troubleshooting:**
- Check this guide
- Install system SDL2 libraries if needed
- Use pre-built pygame wheels when possible

Enjoy playing The Simpsons Arcade Game!
