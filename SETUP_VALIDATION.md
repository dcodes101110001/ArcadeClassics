# Setup Validation and Troubleshooting Guide

This guide helps you verify your installation and troubleshoot common issues with The Simpsons Arcade Game.

## Quick Verification

Run the dependency verification script to check your installation:

```bash
python verify_dependencies.py
```

This will test:
- ✓ pygame and SDL installation
- ✓ streamlit installation
- ✓ Pillow installation
- ✓ Game module imports
- ✓ SDL configuration

If all tests pass, you're ready to play!

## Python Version Requirements

**Supported Python Versions:**
- Python 3.8, 3.9, 3.10, 3.11, 3.12 ✅ (Recommended: 3.12)
- Python 3.13 ✅ (Requires pygame 2.6.1+, included in requirements.txt)

**Check your Python version:**
```bash
python3 --version
```

## Common Issues and Solutions

### 1. pygame Wheel Build Failures

**Symptoms:**
- Error: `_PyLong_AsByteArray` missing arguments
- Error: `subprocess-exited-with-error`
- Error: `Failed building wheel for pygame`

**Cause:** 
Using Python 3.13 with pygame versions older than 2.6.1, or missing SDL2 libraries when building from source.

**Solution:**

**Option A - Install from requirements.txt (Recommended):**
```bash
# Ensure you're using the correct dependencies
pip install -r requirements.txt --upgrade
```

**Option B - Downgrade Python (if Option A fails):**
```bash
# Using pyenv
pyenv install 3.12.3
pyenv local 3.12.3

# Using conda
conda create -n arcade python=3.12
conda activate arcade
pip install -r requirements.txt
```

**Option C - Force pre-built wheels:**
```bash
pip install --upgrade pip
pip install pygame==2.6.1 --only-binary :all:
```

### 2. SDL2 Configuration Errors

**Symptoms:**
- Error: `sdl2-config: not found`
- Error: `SDL.h: No such file or directory`

**Cause:**
pygame trying to build from source without system SDL2 libraries installed.

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev

pip install -r requirements.txt
```

**macOS:**
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
pip install -r requirements.txt
```

**Windows:**
Pre-built pygame wheels include SDL2 DLLs, so no additional installation needed. Just run:
```bash
pip install -r requirements.txt
```

### 3. Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'pygame'
ModuleNotFoundError: No module named 'streamlit'
ModuleNotFoundError: No module named 'PIL'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### 4. Streamlit Cloud Deployment Issues

**Symptoms:**
- Build fails during deployment
- pygame wheel build errors in logs
- Python version mismatch

**Solution:**
Ensure these files are in your repository root:

**1. `runtime.txt`** - Pins Python version
```
python-3.12.3
```

**2. `packages.txt`** - System SDL2 libraries
```
libsdl2-dev
libsdl2-image-dev
libsdl2-mixer-dev
libsdl2-ttf-dev
libfreetype6-dev
libportmidi-dev
```

**3. `requirements.txt`** - Python packages
```
pygame==2.6.1
streamlit>=1.28.0
Pillow>=10.0.0
```

### 5. Display Issues in Headless Environments

**Symptoms:**
- Error: `pygame.error: No available video device`
- Running on CI/CD or server without display

**Solution:**
Set dummy SDL drivers:
```bash
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
python simpsons_arcade.py
```

For Streamlit (which doesn't need display):
```bash
streamlit run streamlit_simpsons_arcade.py --server.headless true
```

## Platform-Specific Notes

### Linux
- ✅ Pre-built wheels work out of the box
- ✅ System SDL2 libraries optional but recommended
- ✅ Tested on Ubuntu 20.04, 22.04, 24.04

### macOS
- ✅ Pre-built wheels work out of the box
- ✅ Homebrew SDL2 libraries optional
- ✅ Tested on macOS 12+

### Windows
- ✅ Pre-built wheels include all SDL2 DLLs
- ✅ No additional installation needed
- ✅ Tested on Windows 10, 11

### Streamlit Cloud
- ✅ Fully supported
- ✅ Use `runtime.txt` to pin Python version
- ✅ Use `packages.txt` for system libraries
- ✅ Pre-built wheels preferred

## Verification Checklist

Before running the game, verify:

- [ ] Python version is 3.8-3.12 (or 3.13 with pygame 2.6.1+)
- [ ] All dependencies installed: `pip list | grep -E "(pygame|streamlit|Pillow)"`
- [ ] pygame version is 2.6.1: `python -c "import pygame; print(pygame.version.ver)"`
- [ ] Verification script passes: `python verify_dependencies.py`

## Testing Your Installation

### Test pygame version:
```bash
python simpsons_arcade.py
```
- Should show character selection menu
- Press ESC to quit

### Test Streamlit version:
```bash
streamlit run streamlit_simpsons_arcade.py
```
- Should open in browser
- Shows character selection screen

## Still Having Issues?

1. **Check Python version**: `python3 --version`
2. **Check pygame version**: `python -c "import pygame; print(pygame.version.ver)"`
3. **Check SDL version**: `python -c "import pygame; print(pygame.version.SDL)"`
4. **Run verification**: `python verify_dependencies.py`
5. **Check installation log**: Look for error messages during `pip install`

## Getting Help

If issues persist after following this guide:

1. **Review the full deployment guide**: See `DEPLOYMENT.md`
2. **Check Streamlit docs**: https://docs.streamlit.io/
3. **Check pygame docs**: https://www.pygame.org/docs/
4. **Verify environment**: Use a fresh virtual environment

## Environment Setup Best Practices

### Using Virtual Environments

**venv (Python built-in):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**conda:**
```bash
conda create -n arcade python=3.12
conda activate arcade
pip install -r requirements.txt
```

**pyenv:**
```bash
pyenv install 3.12.3
pyenv local 3.12.3
pip install -r requirements.txt
```

### Clean Installation

If you have dependency conflicts:
```bash
# Remove old installations
pip uninstall pygame streamlit Pillow -y

# Clear pip cache
pip cache purge

# Reinstall from requirements
pip install -r requirements.txt
```

## Summary

**For most users:**
```bash
python3 --version  # Should be 3.8-3.12 (3.12 recommended)
pip install -r requirements.txt
python verify_dependencies.py
streamlit run streamlit_simpsons_arcade.py
```

**For Streamlit Cloud:**
- Ensure `runtime.txt`, `packages.txt`, and `requirements.txt` are in repo root
- Deploy and let Streamlit Cloud handle the rest

**For troubleshooting:**
- Follow the solutions in this guide
- Check Python version compatibility
- Verify pygame version is 2.6.1
- Use pre-built wheels when possible
