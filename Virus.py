import win32gui
import win32api
import win32con
import win32ui
import win32security
import win32process
import win32file
import win32pipe
import win32event
import win32profile
import win32net
import win32service
import win32serviceutil
import win32evtlog
import win32evtlogutil
import win32clipboard
import win32com.client
import random
import time
import threading
import math
import ctypes
import os
import sys
import subprocess
from ctypes import wintypes
from ctypes import *
import winsound


def clear_effects_nuclear():
    global threads
    threads.clear()
    
    user32.RedrawWindow(0, None, None, 
                       win32con.RDW_INVALIDATE | win32con.RDW_ERASE | 
                       win32con.RDW_ALLCHILDREN | win32con.RDW_FRAME | 
                       win32con.RDW_UPDATENOW | win32con.RDW_ERASENOW)
    
    try:
        progman = win32gui.FindWindow("Progman", None)
        if progman:
            win32gui.ShowWindow(progman, win32con.SW_HIDE)
            win32gui.ShowWindow(progman, win32con.SW_SHOW)
    except:
        pass
    
    try:
        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        if taskbar:
            win32gui.ShowWindow(taskbar, win32con.SW_HIDE)
            win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
    except:
        pass
    
    pos = win32api.GetCursorPos()
    win32api.SetCursorPos((pos[0] + 1, pos[1]))
    win32api.SetCursorPos(pos)
    
    for _ in range(3):
        user32.InvalidateRect(0, None, True)
        user32.UpdateWindow(0)
        time.sleep(0.05)
    
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
    gdi32.BitBlt(hdc, 0, 0, w, h, hdc_mem, 0, 0, SRCCOPY)
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

clear_effects = clear_effects_nuclear

def make_fullscreen():
    global screen_width, screen_height
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    user32.InvalidateRect(0, None, True)
    user32.UpdateWindow(0)

import pygame
import os

pygame.mixer.init()

def stop_xp_remix():
    try:
        subprocess.Popen('taskkill /f /im wmplayer.exe', 
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

HWND_DESKTOP = 0
SRCCOPY = 0x00CC0020
PATINVERT = 0x005A0049
BLACKNESS = 0x00000042
WHITENESS = 0x00FF0062
M_PI = 3.1415926535

user32 = windll.user32
gdi32 = windll.gdi32
kernel32 = windll.kernel32

ctypes.windll.user32.SetProcessDPIAware()

screen_x = user32.GetSystemMetrics(76)
screen_y = user32.GetSystemMetrics(77)
screen_width = user32.GetSystemMetrics(78)
screen_height = user32.GetSystemMetrics(79)

threads = []

def run_effect_duration(func, duration):
    stop_event = threading.Event()
    
    def wrapped():
        start_time = time.time()
        while time.time() - start_time < duration and not stop_event.is_set():
            func()
    
    thread = threading.Thread(target=wrapped)
    thread.daemon = True
    thread.start()
    return thread, stop_event

def start_effect_duration(func, duration):
    thread, _ = run_effect_duration(func, duration)
    threads.append(thread)
    return thread

def kill_everything():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass

    try:
        clear_effects()
    except:
        pass

    os._exit(0)


def monitor_music():
    while True:
        if not pygame.mixer.music.get_busy():
            kill_everything()
        time.sleep(0.5)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def set_wallpaper():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    wallpaper = os.path.join(base_path, "bg.png")

    ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper, 3)


def shader_glitch1_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    try:
        gdi32.BitBlt(hdc, random.randint(-50, 50), random.randint(-50, 50), 
                    w, h, hdc, 0, 0, win32con.SRCINVERT)
        time.sleep(0.01)
    except:
        pass
    user32.ReleaseDC(0, hdc)

def shader_glitch1(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_glitch1_iteration()
    else:
        while True:
            shader_glitch1_iteration()

def shader_glitch2_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    r, g, b = 255, 0, 0
    stage = 0
    
    try:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        if stage == 0:
            g += 5
            if g >= 255: stage = 1
        elif stage == 1:
            r -= 5
            if r <= 0: stage = 2
        elif stage == 2:
            b += 5
            if b >= 255: stage = 3
        elif stage == 3:
            g -= 5
            if g <= 0: stage = 4
        elif stage == 4:
            r += 5
            if r >= 255: stage = 5
        elif stage == 5:
            b -= 5
            if b <= 0: stage = 0
        
        brush = gdi32.CreateSolidBrush(win32api.RGB(r, g, b))
        gdi32.SelectObject(hdc, brush)
        gdi32.BitBlt(hdc, 0, 0, w, h, hdc_mem, 0, 0, win32con.PATINVERT)
        gdi32.DeleteObject(brush)
        
        time.sleep(0.03)
    except:
        pass
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def shader_glitch2(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_glitch2_iteration()
    else:
        while True:
            shader_glitch2_iteration()

def shader_wave_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    offset = 0
    
    try:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        for y in range(0, h, 4):
            wave = int(math.sin((y + offset) * 0.05) * 30)
            gdi32.BitBlt(hdc, wave, y, w, 4, hdc_mem, 0, y, SRCCOPY)
        
        offset += 5
        time.sleep(0.02)
    except:
        pass
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def shader_wave(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_wave_iteration()
    else:
        while True:
            shader_wave_iteration()

def shader_pixel_shuffle_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    try:
        for _ in range(10):
            x = random.randint(0, w-100)
            y = random.randint(0, h-100)
            width = random.randint(50, 200)
            height = random.randint(50, 200)
            
            gdi32.BitBlt(hdc, x + random.randint(-30, 30), y + random.randint(-30, 30), 
                        width, height, hdc, x, y, SRCCOPY)
        
        time.sleep(0.05)
    except:
        pass
    user32.ReleaseDC(0, hdc)

def shader_pixel_shuffle(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_pixel_shuffle_iteration()
    else:
        while True:
            shader_pixel_shuffle_iteration()

def shader_tearing_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    try:
        for i in range(0, h, random.randint(20, 100)):
            gdi32.BitBlt(hdc, random.randint(-20, 20), i, w, 10, 
                        hdc, 0, i, SRCCOPY)
        
        time.sleep(0.02)
    except:
        pass
    user32.ReleaseDC(0, hdc)

def shader_tearing(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_tearing_iteration()
    else:
        while True:
            shader_tearing_iteration()

def shader_rgb_shift_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    try:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        offset = random.randint(5, 20)
        
        gdi32.BitBlt(hdc, offset, 0, w, h, hdc_mem, 0, 0, SRCCOPY)
        gdi32.BitBlt(hdc, -offset, 0, w, h, hdc_mem, 0, 0, SRCCOPY)
        
        time.sleep(0.03)
    except:
        pass
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def shader_rgb_shift(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_rgb_shift_iteration()
    else:
        while True:
            shader_rgb_shift_iteration()

def shader_invert_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    try:
        x = random.randint(0, w-200)
        y = random.randint(0, h-200)
        width = random.randint(100, 400)
        height = random.randint(100, 400)
        
        gdi32.BitBlt(hdc, x, y, width, height, hdc, x, y, win32con.NOTSRCCOPY)
        time.sleep(0.1)
    except:
        pass
    user32.ReleaseDC(0, hdc)

def shader_invert(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_invert_iteration()
    else:
        while True:
            shader_invert_iteration()

def shader_scanlines_iteration():
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    try:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        for y in range(0, h, 4):
            gdi32.BitBlt(hdc, 0, y, w, 2, hdc_mem, 0, y, SRCCOPY)
        
        time.sleep(0.02)
    except:
        pass
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def shader_scanlines(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            shader_scanlines_iteration()
    else:
        while True:
            shader_scanlines_iteration()


def cursor_troll_iteration():
    icon_error = user32.LoadIconW(0, win32con.IDI_ERROR)
    
    try:
        pos = win32api.GetCursorPos()
        
        new_x = pos[0] + random.randint(-5, 5)
        new_y = pos[1] + random.randint(-5, 5)
        win32api.SetCursorPos((new_x, new_y))
        
        hdc = user32.GetDC(0)
        user32.DrawIconEx(
    hdc,
    pos[0] - 16,
    pos[1] - 16,
    icon_error,
    32,
    32,
    0,
    0,
    0x0003
)
        user32.ReleaseDC(0, hdc)
        
        time.sleep(0.02)
    except:
        pass

def cursor_troll(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            cursor_troll_iteration()
    else:
        while True:
            cursor_troll_iteration()


def create_real_error_box(title, message, style=win32con.MB_OK | win32con.MB_ICONERROR):
    
    def show_box():
        time.sleep(random.random())
        ctypes.windll.user32.MessageBoxW(0, message, title, style | win32con.MB_TOPMOST)
    
    thread = threading.Thread(target=show_box)
    thread.daemon = True
    thread.start()
    return thread

def error_spam():
    errors = [
        ("Windows XP System Error", "The system has detected a critical error."),
        ("Windows XP Warning", "A virus has been detected in system32."),
        ("Windows XP - No Disk", "There is no disk in the drive. Please insert a disk."),
        ("Windows XP - Application Error", "The instruction at 0x77f41d24 referenced memory at 0x00000000."),
        ("Windows XP - Explorer.exe", "Explorer.exe has encountered a problem and needs to close."),
        ("Windows XP - Rundll", "Error loading C:\\WINDOWS\\system32\\virus.dll"),
        ("Windows XP - Critical Error", "The system is running low on resources."),
        ("Windows XP - Security Alert", "A program is trying to access your files."),
        ("Windows XP - Blue Screen", "A problem has been detected. Windows has been shut down."),
        ("Windows XP - Installation Error", "Setup cannot continue because the file 'winlogon.exe' is corrupted."),
    ]
    
    while True:
        try:
            for _ in range(random.randint(1, 3)):
                title, msg = random.choice(errors)
                create_real_error_box(f"⚠️ {title}", f"{msg}\n\nError Code: 0x{random.randint(1000, 9999):X}", 
                                    win32con.MB_OK | win32con.MB_ICONERROR)
            
            time.sleep(random.uniform(0.5, 2))
        except:
            pass


def window_chaos_iteration():
    def enum_windows_callback(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            try:
                if random.random() < 0.3:
                    x = random.randint(-100, screen_width)
                    y = random.randint(-100, screen_height)
                    width = random.randint(100, screen_width)
                    height = random.randint(100, screen_height)
                    win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 
                                        win32con.SWP_NOZORDER)
                
                if random.random() < 0.1:
                    win32gui.FlashWindow(hwnd, True)
            except:
                pass
        return True
    
    win32gui.EnumWindows(enum_windows_callback, None)
    time.sleep(0.5)

def window_chaos(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            window_chaos_iteration()
    else:
        while True:
            window_chaos_iteration()

def taskbar_chaos_iteration():
    taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
    try:
        if random.random() < 0.3:
            win32gui.ShowWindow(taskbar, random.choice([win32con.SW_HIDE, win32con.SW_SHOW]))
        time.sleep(2)
    except:
        pass

def taskbar_chaos(duration=None):
    if duration:
        end_time = time.time() + duration
        while time.time() < end_time:
            taskbar_chaos_iteration()
    else:
        while True:
            taskbar_chaos_iteration()

def effect_invert_full(duration=0.1):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        gdi32.BitBlt(hdc, 0, 0, w, h, hdc, 0, 0, win32con.NOTSRCCOPY)
        time.sleep(0.01)
    
    user32.ReleaseDC(0, hdc)

def effect_invert_area(duration=0.1):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        x = random.randint(0, w-200)
        y = random.randint(0, h-200)
        width = random.randint(100, 400)
        height = random.randint(100, 400)
        gdi32.BitBlt(hdc, x, y, width, height, hdc, x, y, win32con.NOTSRCCOPY)
        time.sleep(0.05)
    
    user32.ReleaseDC(0, hdc)

def effect_color_cycle(duration=1):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    colors = [
        win32api.RGB(255, 0, 0),    # Red
        win32api.RGB(0, 255, 0),    # Green
        win32api.RGB(0, 0, 255),    # Blue
        win32api.RGB(255, 255, 0),  # Yellow
        win32api.RGB(255, 0, 255),  # Purple
        win32api.RGB(0, 255, 255),  # Cyan
    ]
    
    end_time = time.time() + duration
    color_index = 0
    
    while time.time() < end_time:
        brush = gdi32.CreateSolidBrush(colors[color_index])
        rect = wintypes.RECT(0, 0, w, h)
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        gdi32.DeleteObject(brush)
        user32.UpdateWindow(0)
        
        color_index = (color_index + 1) % len(colors)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_monochrome(duration=1):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        color = win32api.RGB(255, 255, 255) if int(time.time() * 2) % 2 == 0 else win32api.RGB(0, 0, 0)
        brush = gdi32.CreateSolidBrush(color)
        rect = wintypes.RECT(0, 0, w, h)
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        gdi32.DeleteObject(brush)
        user32.UpdateWindow(0)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_rgb_strobe(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    colors = [win32api.RGB(255,0,0), win32api.RGB(0,255,0), win32api.RGB(0,0,255)]
    
    end_time = time.time() + duration
    color_index = 0
    
    while time.time() < end_time:
        brush = gdi32.CreateSolidBrush(colors[color_index])
        rect = wintypes.RECT(0, 0, w, h)
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        gdi32.DeleteObject(brush)
        user32.UpdateWindow(0)
        
        color_index = (color_index + 1) % len(colors)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_color_bars(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    bar_width = w // 8
    colors = [
        win32api.RGB(255,0,0), win32api.RGB(255,255,0), win32api.RGB(0,255,0),
        win32api.RGB(0,255,255), win32api.RGB(0,0,255), win32api.RGB(255,0,255),
        win32api.RGB(255,255,255), win32api.RGB(0,0,0)
    ]
    
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for i in range(8):
            brush = gdi32.CreateSolidBrush(colors[i])
            rect = wintypes.RECT(i * bar_width, 0, (i + 1) * bar_width, h)
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)
        user32.UpdateWindow(0)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_negative_photo(duration=1):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        hdc_mem = gdi32.CreateCompatibleDC(hdc)
        hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(hdc_mem, hbm)
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        gdi32.BitBlt(hdc, 0, 0, w, h, hdc_mem, 0, 0, win32con.NOTSRCCOPY)
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbm)
        time.sleep(0.05)
    
    user32.ReleaseDC(0, hdc)

def effect_pulse(duration=3):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    direction = 1
    i = 0
    
    while time.time() < end_time:
        brush = gdi32.CreateSolidBrush(win32api.RGB(i, i, i))
        rect = wintypes.RECT(0, 0, w, h)
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        gdi32.DeleteObject(brush)
        
        i += direction * 5
        if i >= 255:
            i = 255
            direction = -1
        elif i <= 0:
            i = 0
            direction = 1
        
        time.sleep(0.02)
    
    user32.ReleaseDC(0, hdc)

def effect_swap_rb(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        hdc_mem = gdi32.CreateCompatibleDC(hdc)
        hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(hdc_mem, hbm)
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        for y in range(0, h, 2):
            gdi32.BitBlt(hdc, 5, y, w, 1, hdc_mem, 0, y, SRCCOPY)
            gdi32.BitBlt(hdc, -5, y+1, w, 1, hdc_mem, 0, y+1, SRCCOPY)
        
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbm)
        time.sleep(0.05)
    
    user32.ReleaseDC(0, hdc)

def effect_solarize(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    toggle = True
    
    while time.time() < end_time:
        hdc_mem = gdi32.CreateCompatibleDC(hdc)
        hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(hdc_mem, hbm)
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        if toggle:
            gdi32.BitBlt(hdc, 0, 0, w, h, hdc_mem, 0, 0, win32con.NOTSRCCOPY)
        
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbm)
        
        toggle = not toggle
        time.sleep(0.2)
    
    user32.ReleaseDC(0, hdc)

def effect_halftone(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        brush = gdi32.CreateSolidBrush(win32api.RGB(128, 128, 128))
        gdi32.SetBkMode(hdc, win32con.TRANSPARENT)
        
        for x in range(0, w, 20):
            for y in range(0, h, 20):
                rect = wintypes.RECT(x, y, x+5, y+5)
                user32.FillRect(hdc, ctypes.byref(rect), brush)
        
        gdi32.DeleteObject(brush)
        user32.UpdateWindow(0)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_xor_pattern(duration=2):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    end_time = time.time() + duration
    while time.time() < end_time:
        hdc_mem = gdi32.CreateCompatibleDC(hdc)
        hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(hdc_mem, hbm)
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        gdi32.BitBlt(hdc, 10, 10, w-20, h-20, hdc_mem, 10, 10, win32con.SRCINVERT)
        
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbm)
        user32.UpdateWindow(0)
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)



def effect_bouncing_boxes(duration=5):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    boxes = []
    for i in range(8):
        boxes.append({
            'x': random.randint(0, w-100),
            'y': random.randint(0, h-100),
            'width': random.randint(50, 150),
            'height': random.randint(50, 150),
            'dx': random.choice([-8, -6, -4, 4, 6, 8]),
            'dy': random.choice([-8, -6, -4, 4, 6, 8]),
            'color': win32api.RGB(random.randint(100,255), random.randint(100,255), random.randint(100,255))
        })
    
    end_time = time.time() + duration
    while time.time() < end_time:
        hdc_mem = gdi32.CreateCompatibleDC(hdc)
        hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(hdc_mem, hbm)
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        for box in boxes:
            box['x'] += box['dx']
            box['y'] += box['dy']
            
            if box['x'] <= 0 or box['x'] + box['width'] >= w:
                box['dx'] = -box['dx']
                box['color'] = win32api.RGB(random.randint(100,255), random.randint(100,255), random.randint(100,255))
            if box['y'] <= 0 or box['y'] + box['height'] >= h:
                box['dy'] = -box['dy']
                box['color'] = win32api.RGB(random.randint(100,255), random.randint(100,255), random.randint(100,255))
            
            brush = gdi32.CreateSolidBrush(box['color'])
            rect = wintypes.RECT(int(box['x']), int(box['y']), 
                                int(box['x'] + box['width']), int(box['y'] + box['height']))
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)
        
        gdi32.DeleteDC(hdc_mem)
        gdi32.DeleteObject(hbm)
        time.sleep(0.02)
    
    user32.ReleaseDC(0, hdc)

def effect_spinning_colors(duration=5):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    center_x, center_y = w//2, h//2
    angle = 0
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(8):
            color = win32api.RGB(
                int(128 + 127 * math.sin(angle + i)),
                int(128 + 127 * math.sin(angle + i + 2)),
                int(128 + 127 * math.sin(angle + i + 4))
            )
            brush = gdi32.CreateSolidBrush(color)
            
            path = gdi32.BeginPath(hdc)
            rect = wintypes.RECT(
                int(center_x + math.cos(angle + i) * 200),
                int(center_y + math.sin(angle + i) * 200),
                int(center_x + math.cos(angle + i) * 200 + 50),
                int(center_y + math.sin(angle + i) * 200 + 50)
            )
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)
        
        angle += 0.1
        time.sleep(0.03)
    
    user32.ReleaseDC(0, hdc)

def effect_earthquake(duration=3):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    end_time = time.time() + duration
    while time.time() < end_time:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        offset_x = random.randint(-30, 30)
        offset_y = random.randint(-30, 30)
        gdi32.BitBlt(hdc, offset_x, offset_y, w, h, hdc_mem, 0, 0, SRCCOPY)
        
        time.sleep(0.03)
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def effect_zoom_boxes(duration=4):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    boxes = []
    for i in range(5):
        boxes.append({
            'x': random.randint(100, w-200),
            'y': random.randint(100, h-200),
            'size': 50,
            'grow': True,
            'speed': random.uniform(1, 3)
        })
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for box in boxes:
            if box['grow']:
                box['size'] += box['speed']
                if box['size'] > 150:
                    box['grow'] = False
            else:
                box['size'] -= box['speed']
                if box['size'] < 30:
                    box['grow'] = True
            
            color = win32api.RGB(
                int(255 * (box['size']/150)),
                int(255 * (1 - box['size']/150)),
                int(128 + 127 * math.sin(time.time()))
            )
            
            brush = gdi32.CreateSolidBrush(color)
            rect = wintypes.RECT(
                int(box['x'] - box['size']/2),
                int(box['y'] - box['size']/2),
                int(box['x'] + box['size']/2),
                int(box['y'] + box['size']/2)
            )
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)
        
        time.sleep(0.02)
    
    user32.ReleaseDC(0, hdc)

def effect_tunnel(duration=4):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    center_x, center_y = w//2, h//2
    size = 0
    
    end_time = time.time() + duration
    while time.time() < end_time:
        size = (size + 10) % (w//2)
        color = win32api.RGB(
            int(128 + 127 * math.sin(time.time())),
            int(128 + 127 * math.sin(time.time() + 2)),
            int(128 + 127 * math.sin(time.time() + 4))
        )
        
        brush = gdi32.CreateSolidBrush(color)
        rect = wintypes.RECT(
            center_x - size,
            center_y - size,
            center_x + size,
            center_y + size
        )
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        gdi32.DeleteObject(brush)
        
        time.sleep(0.03)
    
    user32.ReleaseDC(0, hdc)

def effect_sinusoidal_wave(duration=5):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    hdc_mem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, w, h)
    gdi32.SelectObject(hdc_mem, hbm)
    
    offset = 0
    
    end_time = time.time() + duration
    while time.time() < end_time:
        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc, 0, 0, SRCCOPY)
        
        for y in range(0, h, 20):
            wave_offset = int(math.sin((y + offset) * 0.02) * 100)
            gdi32.BitBlt(hdc, wave_offset, y, w, 20, hdc_mem, 0, y, SRCCOPY)
        
        offset += 10
        time.sleep(0.02)
    
    gdi32.DeleteDC(hdc_mem)
    gdi32.DeleteObject(hbm)
    user32.ReleaseDC(0, hdc)

def effect_spiral(duration=4):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    center_x, center_y = w//2, h//2
    angle = 0
    radius = 0
    
    end_time = time.time() + duration
    while time.time() < end_time:
        radius += 2
        angle += 0.1
        
        x = int(center_x + math.cos(angle) * radius)
        y = int(center_y + math.sin(angle) * radius)
        
        if 0 < x < w and 0 < y < h:
            color = win32api.RGB(
                int(128 + 127 * math.sin(angle)),
                int(128 + 127 * math.sin(angle + 2)),
                int(128 + 127 * math.sin(angle + 4))
            )
            
            brush = gdi32.CreateSolidBrush(color)
            rect = wintypes.RECT(x-10, y-10, x+10, y+10)
            user32.FillRect(hdc, ctypes.byref(rect), brush)
            gdi32.DeleteObject(brush)
        
        if radius > max(w, h):
            radius = 0
        
        time.sleep(0.01)
    
    user32.ReleaseDC(0, hdc)

def effect_mosaic(duration=4):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    tile_size = 50
    cols = w // tile_size
    rows = h // tile_size
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for i in range(cols):
            for j in range(rows):
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 20)
                
                gdi32.BitBlt(hdc, 
                            i*tile_size + offset_x, 
                            j*tile_size + offset_y, 
                            tile_size, tile_size, 
                            hdc, 
                            i*tile_size, j*tile_size, 
                            SRCCOPY)
        
        time.sleep(0.1)
    
    user32.ReleaseDC(0, hdc)

def effect_rainbow_swirl(duration=5):
    hdc = user32.GetDC(0)
    w, h = screen_width, screen_height
    
    angle = 0
    
    end_time = time.time() + duration
    while time.time() < end_time:
        for x in range(0, w, 20):
            for y in range(0, h, 20):
                r = int(128 + 127 * math.sin(x * 0.01 + angle))
                g = int(128 + 127 * math.sin(y * 0.01 + angle + 2))
                b = int(128 + 127 * math.sin((x+y) * 0.01 + angle + 4))
                
                brush = gdi32.CreateSolidBrush(win32api.RGB(r, g, b))
                rect = wintypes.RECT(x, y, x+20, y+20)
                user32.FillRect(hdc, ctypes.byref(rect), brush)
                gdi32.DeleteObject(brush)
        
        angle += 0.05
        time.sleep(0.0003)
    
    user32.ReleaseDC(0, hdc)


def msg_snare():
    def show():
        ctypes.windll.user32.MessageBoxW(0, 
            "SNARE!", 
            "⚠️ BEAT", 
            win32con.MB_OK | win32con.MB_ICONERROR | win32con.MB_TOPMOST)
    thread = threading.Thread(target=show)
    thread.daemon = True
    thread.start()

def msg_kick():
    def show():
        ctypes.windll.user32.MessageBoxW(0, 
            "KICK!", 
            "⚠️ BEAT", 
            win32con.MB_OK | win32con.MB_ICONWARNING | win32con.MB_TOPMOST)
    thread = threading.Thread(target=show)
    thread.daemon = True
    thread.start()

def msg_crash():
    def show():
        ctypes.windll.user32.MessageBoxW(0, 
            "CRASH", 
            "BEAT", 
            win32con.MB_OK | win32con.MB_ICONHAND | win32con.MB_TOPMOST)
    thread = threading.Thread(target=show)
    thread.daemon = True
    thread.start()

def msg_custom(text, title="Windows XP"):
    def show():
        ctypes.windll.user32.MessageBoxW(0, text, title, win32con.MB_OK | win32con.MB_TOPMOST)
    thread = threading.Thread(target=show)
    thread.daemon = True
    thread.start()

def start_effect(func, duration=None):
    if duration is not None:
        if func in [shader_glitch1, shader_glitch2, shader_wave, shader_pixel_shuffle, 
                   shader_tearing, shader_rgb_shift, shader_invert, shader_scanlines,
                   cursor_troll, window_chaos, taskbar_chaos]:
            thread = threading.Thread(target=func, args=(duration,))
        else:
            func(duration)
            return
    else:
        thread = threading.Thread(target=func)
    
    thread.daemon = True
    thread.start()
    threads.append(thread)
    return thread


def main():
    try:
        console = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(console, win32con.SW_HIDE)
    except:
        pass
    
    result = ctypes.windll.user32.MessageBoxW(0, 
        "Do you want to start the Windows XP Virus?\nEpilepsy Warning!\n\nAuthor: -Void", 
        "⚠️ Security Alert", 
        win32con.MB_YESNO | win32con.MB_ICONWARNING | win32con.MB_TOPMOST)

    if result == 6:
        try:
            os.system("taskkill /f /im wallpaper32.exe /t")
            os.system("taskkill /f /im wallpaper64.exe /t")
            set_wallpaper()
            mp3_path = resource_path("xp_remix.mp3")
            pygame.mixer.music.load(mp3_path)
            pygame.mixer.music.play()

            threading.Thread(target=monitor_music, daemon=True).start()
        except:
            pass
        user32.SetWindowPos(0, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        
        time.sleep(4)
        #1error box
        start_effect(cursor_troll,100)
        time.sleep(3.5)
        start_effect(shader_glitch1,5)
        time.sleep(5.5)
        clear_effects()
        start_effect(shader_glitch2,5.3) #flashing
        time.sleep(5.3)
        start_effect(shader_wave,5) #wave screen left right
        time.sleep(1)
        start_effect(shader_pixel_shuffle,5)# Distort screen in boxes
        time.sleep(1)
        start_effect(shader_tearing,3.2)# screen tearing
        time.sleep(2.7)
        clear_effects()
        start_effect(shader_rgb_shift,4.7)
        time.sleep(4.7)
        clear_effects()
        #start_effect(error_spam,5)
        #start_effect(window_chaos)
        #start_effect(taskbar_chaos)

        effect_invert_full(1.6)      # Full screen invert for 5 seconds
        time.sleep(1.6)
        clear_effects()
        effect_invert_area(2.7)      # Random area invert for 5 seconds
        time.sleep(2.7)
        clear_effects()
        #effect_color_cycle(1)      # Random color flash for 5 seconds
        #time.sleep(1)
        #clear_effects()
        #effect_monochrome(1)       # Black/white flash for 5 seconds
        #time.sleep(1)
        clear_effects()
        effect_rgb_strobe(2.3)       # RGB strobe sequence for 5 seconds
        time.sleep(2.3)
        clear_effects()
        effect_color_bars(1)       # TV color bars for 5 seconds
        time.sleep(1)
        clear_effects()
        effect_negative_photo(1.1)   # Photo negative for 5 seconds
        time.sleep(0.8)
        clear_effects()
        #effect_pulse(0.8)            # Brightness pulse for 5 seconds
        #time.sleep(0.8)
        clear_effects()
        effect_swap_rb(3)          # Swap red/blue for 5 seconds
        time.sleep(3)
        clear_effects()
        effect_solarize(3)         # Solarize effect for 5 seconds
        time.sleep(3)
   #     clear_effects()
   #     effect_halftone(3)         # Halftone pattern for 5 seconds
   #     time.sleep(3)
        clear_effects()
        #effect_xor_pattern(1.5)      # XOR pattern for 5 seconds
        #time.sleep(1.5)
        #clear_effects()
        # Movement effects (each runs for X seconds)
        #effect_bouncing_boxes(3)      # RGB boxes bounce around for 8 seconds
        #time.sleep(3)
        #clear_effects()
        #effect_earthquake(2)          # Screen shakes for 4 seconds
        #time.sleep(1.5)
        #clear_effects()
        #effect_zoom_boxes(1.5)          # Boxes zoom in/out for 5 seconds  
        #time.sleep(1.5)
        #clear_effects()
        effect_tunnel(0.7)              # Tunnel vision for 4 seconds
        time.sleep(0.7)
        clear_effects()
        effect_sinusoidal_wave(2.7)     # Wave moves across screen for 6 seconds
        time.sleep(2.7)
        clear_effects()
        effect_spiral(1.6)              # Spiral draws for 5 seconds
        time.sleep(1.6)
        clear_effects()
        effect_mosaic(2)              # Tiles shift for 4 seconds
        time.sleep(2)
        clear_effects()
        effect_rainbow_swirl(3)       # Swirling rainbow for 7 seconds
        time.sleep(3)
        clear_effects()
        try:
            import keyboard
            print("Press ESC to stop...")
            keyboard.wait('esc')
        except:
            time.sleep(60)
    else:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass

    global threads
    for t in threads:
        try:
            if t.is_alive():
                t.join(timeout=0.1)
        except:
            pass
    threads.clear()

    try:
        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
    except:
        pass

    os._exit(0)
    
    stop_xp_remix()
    
    try:
        taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
        win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)