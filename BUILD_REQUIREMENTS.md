# Build Requirements and Dependency Resolution Guide

This document provides comprehensive information about building and installing the Simpsons Arcade Game project, with specific focus on resolving pygame build issues and ensuring smooth installation across different platforms.

## Table of Contents
- [Python Version Requirements](#python-version-requirements)
- [Build Tools Requirements](#build-tools-requirements)
- [Package Dependencies](#package-dependencies)
- [System Dependencies](#system-dependencies)
- [Troubleshooting Build Failures](#troubleshooting-build-failures)
- [Platform-Specific Build Notes](#platform-specific-build-notes)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)

## Python Version Requirements

### Supported Python Versions

| Python Version | pygame 2.6.1 | Status | Notes |
|---------------|--------------|--------|-------|
| 3.7 | ⚠️ | May work | Not officially tested |
| 3.8 | ✅ | Fully supported | Tested |
| 3.9 | ✅ | Fully supported | Tested |
| 3.10 | ✅ | Fully supported | Tested |
| 3.11 | ✅ | Fully supported | Tested |
| 3.12 | ✅ | **Recommended** | Tested, most stable |
| 3.13 | ✅ | Supported | Requires pygame 2.6.1+ |

### Version Verification

Check your Python version:
```bash
python3 --version
```

If using Python 3.13 or encountering build issues, ensure you're using Python 3.12:
```bash
# Using pyenv
pyenv install 3.12.3
pyenv local 3.12.3

# Using conda
conda create -n arcade python=3.12
conda activate arcade
```

## Build Tools Requirements

### Essential Build Tools

Before installing the project dependencies, ensure you have up-to-date build tools:

```bash
# Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel
```

### Minimum Versions

| Tool | Minimum Version | Recommended Version | Purpose |
|------|----------------|---------------------|---------|
| pip | 23.0 | Latest | Package installer with modern wheel support |
| setuptools | 65.0 | Latest | Package building and distribution |
| wheel | 0.40.0 | Latest | Binary distribution format |

### Verification Script

Check your build tools:
```bash
python -c "import pip, setuptools, wheel; print(f'pip: {pip.__version__}\nsetuptools: {setuptools.__version__}\nwheel: {wheel.__version__}')"
```

## Package Dependencies

### Python Package Dependencies

All Python packages are specified in `requirements.txt`:

1. **pygame 2.6.1**
   - Pre-built wheels available for most platforms
   - Includes SDL2 2.28.x libraries bundled
   - Critical for Python 3.13 compatibility

2. **streamlit >= 1.28.0**
   - Web framework for browser-based game version
   - No special build requirements

3. **Pillow >= 10.0.0**
   - Image processing library
   - Pre-built wheels available

### Installation

```bash
pip install -r requirements.txt
```

### Forced Pre-built Wheels

If you encounter build issues, force pip to use only pre-built wheels:

```bash
pip install --only-binary :all: -r requirements.txt
```

## System Dependencies

### SDL2 Libraries (Optional for Pre-built Wheels)

While pygame 2.6.1 pre-built wheels include SDL2 libraries, some scenarios require system SDL2:

1. Building pygame from source (no wheel available)
2. Certain pygame features requiring system libraries
3. Streamlit Cloud deployment (packages.txt)
4. Development/debugging with system SDL

### Required SDL2 Libraries

The following system libraries are needed when building pygame from source:

- **libsdl2-dev** - SDL2 core library (graphics, input, audio)
- **libsdl2-image-dev** - SDL2 image loading (PNG, JPG, etc.)
- **libsdl2-mixer-dev** - SDL2 audio mixing
- **libsdl2-ttf-dev** - SDL2 TrueType font rendering
- **libfreetype6-dev** - Font rendering library
- **libportmidi-dev** - MIDI support for pygame

### Platform-Specific Installation

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
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y \
    SDL2-devel \
    SDL2_image-devel \
    SDL2_mixer-devel \
    SDL2_ttf-devel \
    freetype-devel \
    portmidi-devel
```

**macOS (Homebrew):**
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
```

**Windows:**
Pre-built pygame wheels include all SDL2 DLLs. No additional installation needed.

## Troubleshooting Build Failures

### Common Error: pygame Wheel Build Failure

**Symptoms:**
```
ERROR: Failed building wheel for pygame
subprocess-exited-with-error
× Building wheel for pygame (pyproject.toml) did not run successfully.
```

**Causes:**
1. Python 3.13 with pygame < 2.6.1
2. Missing system SDL2 development libraries
3. Outdated pip/setuptools/wheel
4. No pre-built wheel available for your platform

**Solutions (in order of preference):**

1. **Use pre-built wheels with correct pygame version:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install pygame==2.6.1 --only-binary :all:
   pip install -r requirements.txt
   ```

2. **Downgrade Python (if on 3.13 and issues persist):**
   ```bash
   pyenv install 3.12.3
   pyenv local 3.12.3
   pip install -r requirements.txt
   ```

3. **Install system SDL2 libraries then rebuild:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   pip install -r requirements.txt
   ```

### Error: _PyLong_AsByteArray Missing Arguments

**Symptom:**
```
error: too few arguments to function '_PyLong_AsByteArray'
```

**Cause:** 
Using pygame version < 2.6.1 with Python 3.13

**Solution:**
```bash
# Upgrade pygame to 2.6.1+
pip install pygame==2.6.1 --upgrade
```

Or downgrade Python to 3.12:
```bash
pyenv install 3.12.3
pyenv local 3.12.3
```

### Error: sdl2-config Not Found

**Symptom:**
```
sh: 1: sdl2-config: not found
```

**Cause:**
pygame trying to build from source without system SDL2 libraries

**Solution:**

**Option A - Use pre-built wheel (recommended):**
```bash
pip install pygame==2.6.1 --only-binary :all:
```

**Option B - Install system SDL2:**
```bash
# Ubuntu/Debian
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# macOS
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Then install pygame
pip install pygame==2.6.1
```

### Error: No Available Video Device

**Symptom:**
```
pygame.error: No available video device
```

**Cause:**
Running in headless environment (CI/CD, server) without display

**Solution:**
```bash
# Set dummy SDL drivers for headless mode
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
python simpsons_arcade.py

# Or use Streamlit version (doesn't need display)
streamlit run streamlit_simpsons_arcade.py --server.headless true
```

## Platform-Specific Build Notes

### Linux

**Ubuntu 20.04 / 22.04 / 24.04:**
- ✅ Pre-built wheels work out of the box
- ✅ System SDL2 optional but recommended for development
- ✅ Python 3.8-3.12 available via apt
- ✅ Python 3.13 available via deadsnakes PPA

**Arch Linux:**
```bash
sudo pacman -S sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
pip install -r requirements.txt
```

### macOS

**macOS 12+ (Monterey and later):**
- ✅ Pre-built wheels work out of the box
- ✅ Homebrew SDL2 optional
- ✅ Python 3.8-3.12 via Homebrew or pyenv
- ⚠️ M1/M2 ARM: Use native ARM64 Python for best performance

**Installation:**
```bash
# Option 1: Just use wheels (easiest)
pip install -r requirements.txt

# Option 2: Install Homebrew SDL2 (for development)
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
pip install -r requirements.txt
```

### Windows

**Windows 10 / 11:**
- ✅ Pre-built wheels include all SDL2 DLLs
- ✅ No additional dependencies needed
- ✅ Works with Python from python.org or Microsoft Store
- ✅ Works in WSL2 (use Linux instructions for WSL)

**Installation:**
```bash
pip install -r requirements.txt
```

## Streamlit Cloud Deployment

### Required Files

Streamlit Cloud needs three files in the repository root:

1. **requirements.txt** - Python packages
2. **packages.txt** - System apt packages
3. **runtime.txt** - Python version specification

### Configuration Files

**requirements.txt:**
```
pygame==2.6.1
streamlit>=1.28.0
Pillow>=10.0.0
```

**packages.txt:**
```
libsdl2-dev
libsdl2-image-dev
libsdl2-mixer-dev
libsdl2-ttf-dev
libfreetype6-dev
libportmidi-dev
```

**runtime.txt:**
```
python-3.12.3
```

### Why packages.txt is Critical

Streamlit Cloud runs on Debian Linux. While pygame wheels include SDL2, `packages.txt` ensures:
1. System SDL2 libraries available if wheel build needed
2. Fallback compatibility for different pygame versions
3. Support for features requiring system libraries

### Deployment Process

1. **Ensure files are committed:**
   ```bash
   git add requirements.txt packages.txt runtime.txt
   git commit -m "Configure for Streamlit Cloud"
   git push
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to share.streamlit.io
   - Select repository
   - Main file: `streamlit_simpsons_arcade.py`
   - Deploy

3. **Monitor build logs:**
   - Check for pygame installation success
   - Verify Python version matches runtime.txt
   - Ensure all dependencies install without errors

### Debugging Streamlit Cloud Builds

If deployment fails:

1. **Check build logs for errors:**
   - Look for "Failed building wheel for pygame"
   - Check Python version being used
   - Verify packages.txt libraries installed

2. **Common fixes:**
   ```
   # Ensure runtime.txt has exactly:
   python-3.12.3
   
   # Ensure packages.txt has SDL2 libraries
   # Ensure pygame==2.6.1 in requirements.txt
   ```

3. **Test locally first:**
   ```bash
   # Create fresh environment matching Streamlit Cloud
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   streamlit run streamlit_simpsons_arcade.py
   ```

## Environment Validation

### Validation Script

Use the included verification script:
```bash
python verify_dependencies.py
```

This checks:
- ✓ pygame and SDL installation
- ✓ streamlit installation
- ✓ Pillow installation
- ✓ Game module imports
- ✓ SDL configuration

### Manual Validation

**Check Python version:**
```bash
python3 --version
```

**Check pygame version and SDL:**
```bash
python -c "import pygame; print(f'pygame: {pygame.version.ver}, SDL: {pygame.version.SDL}')"
```

**Check all dependencies:**
```bash
pip list | grep -E "(pygame|streamlit|Pillow)"
```

**Test imports:**
```bash
python -c "import pygame, streamlit, PIL; print('All imports successful')"
```

## Best Practices

### Development Environment

1. **Use virtual environments:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. **Pin Python version:**
   ```bash
   # Use pyenv for consistent Python versions
   pyenv install 3.12.3
   pyenv local 3.12.3
   ```

3. **Keep build tools updated:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

### Continuous Integration

For CI/CD environments:

```yaml
# Example GitHub Actions
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    
- name: Test headless
  env:
    SDL_VIDEODRIVER: dummy
    SDL_AUDIODRIVER: dummy
  run: |
    python test_simpsons_arcade.py
```

### Dependency Locking

For reproducible builds, consider creating `requirements-lock.txt`:
```bash
pip freeze > requirements-lock.txt
```

Then install with:
```bash
pip install -r requirements-lock.txt
```

## Summary

**Quick Start for Most Users:**
```bash
python3 --version  # Ensure 3.8-3.12 (3.12 recommended)
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python verify_dependencies.py
```

**For Build Issues:**
1. Update build tools: `pip install --upgrade pip setuptools wheel`
2. Use pre-built wheels: `pip install pygame==2.6.1 --only-binary :all:`
3. If needed, install system SDL2 libraries
4. If all else fails, use Python 3.12

**For Streamlit Cloud:**
- Ensure `requirements.txt`, `packages.txt`, and `runtime.txt` are configured
- Deploy and monitor build logs
- Test locally first with matching Python version

## Additional Resources

- **pygame Documentation:** https://www.pygame.org/docs/
- **SDL2 Documentation:** https://wiki.libsdl.org/
- **Streamlit Documentation:** https://docs.streamlit.io/
- **Python Packaging:** https://packaging.python.org/
- **pip Documentation:** https://pip.pypa.io/
