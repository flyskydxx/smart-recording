'''
author @ Xiaoxiao DONG
date: 20240825
version: 1.0
This script is used to record the window screen and save it to image.
'''

import cv2
import numpy as np
import pygetwindow as gw
import time
import os

def list_windows():
    windows = gw.getAllTitles()
    windows = [win for win in windows if win]  # Filter out empty titles
    for i, win in enumerate(windows):
        print(f"{i + 1}: {win}")
    return windows

def choose_window(windows):
    choice = int(input("Choose a window by number: ")) - 1
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        print("Invalid choice")
        return None

def record_window(window_name, save_path, duration=10, fps=30):
    window = gw.getWindowsWithTitle(window_name)[0]
    window.activate()
    window.resizeTo(1920, 1080)
    window.moveTo(0, 0)

    x, y, width, height = window.left, window.top, window.width, window.height

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    start_time = time.time()
    frame_count = 0
    while time.time() - start_time < duration:
        img = np.array(window.capture())
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_filename = os.path.join(save_path, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_filename, img)
        frame_count += 1
        time.sleep(1 / fps)

if __name__ == "__main__":
    windows = list_windows()
    chosen_window = choose_window(windows)
    if chosen_window:
        save_path = "recorded_images"
        record_window(chosen_window, save_path, duration=10, fps=30)
        print(f"Recording saved to {save_path}")
    else:
        print("No window chosen")