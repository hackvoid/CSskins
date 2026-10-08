#!/usr/bin/env python3
import sys
try:
    import win32gui
    import win32con
    import win32process
except ImportError:
    print("Warning: win32 modules not found. This script is intended for Windows.")

import psutil
import keyboard
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap

# ==========================================
# CONFIGURATION
# ==========================================
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
# ==========================================

class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.is_active = True
        self.initUI()
        
        # Setup hotkeys
        keyboard.add_hotkey(HOTKEY_TOGGLE, self.toggle_visibility)
        keyboard.add_hotkey(HOTKEY_EXIT, self.exit_app)
        
        # Setup a timer to constantly track and snap to the game window
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(16) # ~60 FPS tracking updates

    def initUI(self):
        # 1. Always On Top & Frameless
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool  # Hides it from the taskbar to act purely as an overlay
        )
        
        # 2. Transparent Background (Qt Level)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        
        # Setup the image
        self.label = QLabel(self)
        pixmap = QPixmap(IMAGE_PATH)
        
        # Scale image if needed, maintaining aspect ratio
        pixmap = pixmap.scaled(IMAGE_WIDTH, IMAGE_HEIGHT, 
                               Qt.AspectRatioMode.KeepAspectRatio, 
                               Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(pixmap)
        
        self.resize(pixmap.width(), pixmap.height())
        self.label.resize(pixmap.width(), pixmap.height())

    def showEvent(self, event):
        """Called when the window is shown. We apply Win32 styles here to ensure click-through."""
        super().showEvent(event)
        
        # 3. Apply Win32 WS_EX_TRANSPARENT to pass all inputs through to the game
        try:
            hwnd = int(self.winId())
            ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(
                hwnd, 
                win32con.GWL_EXSTYLE, 
                ex_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST
            )
        except NameError:
            pass # win32gui not imported

    def toggle_visibility(self):
        self.is_active = not self.is_active
        if self.is_active:
            self.show()
        else:
            self.hide()

    def exit_app(self):
        QApplication.quit()

    def get_hwnds_for_pid(self, pid):
        """Helper to find the specific Window Handle (HWND) for the game process."""
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True
        
        hwnds = []
        try:
            win32gui.EnumWindows(callback, hwnds)
        except NameError:
            pass
        return hwnds

    def update_position(self):
        if not self.is_active:
            return

        # 4. Target Matching: Check if hl.exe is running
        target_pid = None
        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if proc.info['name'].lower() == TARGET_EXE.lower():
                    target_pid = proc.info['pid']
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # If running, get its window and match coordinates
        if target_pid:
            hwnds = self.get_hwnds_for_pid(target_pid)
            if hwnds:
                hwnd = hwnds[0]
                try:
                    rect = win32gui.GetWindowRect(hwnd)
                    # Rect gives us: (left, top, right, bottom)
                    left, top, right, bottom = rect
                    
                    # Position overlay at the bottom-right of the game window
                    target_x = right - self.width() - OFFSET_X
                    target_y = bottom - self.height() - OFFSET_Y
                    
                    self.move(target_x, target_y)
                    
                    if self.isHidden():
                        self.show()
                except Exception:
                    pass
        else:
            # Hide the overlay if the game is closed or minimized
            if not self.isHidden():
                self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()
    sys.exit(app.exec())
