# Half-Life / CS 1.6 Image Overlay

A Python-based, transparent, and click-through image overlay designed specifically for `hl.exe` (Half-Life, Counter-Strike 1.6, etc.). It renders a custom image (e.g., weapon skins, crosshairs, or UI elements) directly over your game window.

## Features

* **Targeted Window Tracking**: Automatically tracks the `hl.exe` window and snaps the overlay to its bottom-right corner.
* **Click-Through & Transparent**: The overlay is completely un-clickable and doesn't interfere with your gameplay.
* **Always On Top**: Ensures the overlay stays visible over the game (works best in Windowed or Borderless Windowed mode).
* **Keyboard Hotkeys**: Easily toggle visibility or exit the overlay on the fly.
* **Standalone Executable Support**: Build it into a portable `.exe` file so you don't need Python installed.

## Prerequisites

If you plan to run from source, you need Python 3 installed. The required dependencies are:
- `PyQt6`
- `pywin32`
- `psutil`
- `keyboard`
- `pyinstaller` (only needed for building the `.exe`)

## Usage

### 1. Running from Source (Quick Start)
The easiest way to run the script is using the provided batch file, which automatically handles dependencies and admin privileges (required for hotkeys).

1. Ensure Python is installed and added to your PATH.
2. Ensure your image is named `ak47.png` and placed in the project directory.
3. Double-click `run_overlay.bat`.

Alternatively, you can run it manually via command line:
```cmd
pip install PyQt6 pywin32 psutil keyboard
python overlay.py
```
*(Note: You may need to run your command prompt as Administrator for the global hotkeys to work properly).*

### 2. Building a Standalone Executable
If you want to share the overlay or run it without installing Python:

1. Double-click `build_executable.bat`.
2. Wait for the compilation to finish.
3. A new `dist` folder will be created. 
4. Move your `ak47.png` into the `dist` folder.
5. Right-click `overlay.exe` inside the `dist` folder and select **Run as Administrator**.

## Controls

* **F9** - Toggle overlay visibility (Hide/Show)
* **Ctrl + Shift + O** - Exit the overlay completely

## Configuration

You can change the target executable, image path, hotkeys, and positioning by editing the `CONFIGURATION` section at the top of `overlay.py`:

```python
TARGET_EXE = "hl.exe"
IMAGE_PATH = "ak47.png"

# Hotkeys
HOTKEY_TOGGLE = "F9"
HOTKEY_EXIT = "ctrl+shift+o"

# Image Dimensions
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300

# Positioning (distance from the bottom-right of the game window)
OFFSET_X = 20  
OFFSET_Y = 20  
```

## Important Notes
- **Admin Rights**: The `keyboard` module requires administrative privileges to hook global hotkeys in Windows.
- **Windowed Mode**: Games running in Exclusive Fullscreen mode may draw over the overlay. For best results, run the game in Windowed or Borderless Windowed mode.
- **Anticheat Warning**: While this script only reads window positions and draws a transparent UI element via Windows APIs, some aggressive anti-cheat systems might flag background processes that inject hotkeys or scan process lists. Use at your own risk on secured servers.
