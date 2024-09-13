'''
author @ Xiaoxiao DONG
date: 20240825
version: 1.0
This script is used to record the window screen and save it to image.
'''

import cv2
import numpy as np
import time
import os
from PIL import ImageGrab
from pywinauto import Desktop

def list_windows():
    # Get a list of all windows using pywinauto's Desktop class
    windows = Desktop(backend="uia").windows()
    
    # Print the window text for each window
    for i, win in enumerate(windows):
        print(f"{i + 1}: {win.window_text()}")
    
    return windows

def choose_window(windows):
    # Prompt the user to choose a window by number
    choice = int(input("Choose a window by number: ")) - 1
    
    # Check if the choice is valid
    if 0 <= choice < len(windows):
        return windows[choice]
    else:
        print("Invalid choice")
        return None

def calculate_difference(img1, img2):
    # Convert images to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Calculate the absolute difference
    diff = cv2.absdiff(gray1, gray2)
    
    # Calculate the percentage of different pixels
    non_zero_count = np.count_nonzero(diff)
    total_count = diff.size
    percentage_diff = (non_zero_count / total_count) * 100
    
    return percentage_diff

def record_window(window, save_path, duration=10, fps=30):
    try:
        window.set_focus()
        time.sleep(1)  # Give some time for the window to activate
        rect = window.rectangle()
        
        frame_time = 1 / fps
        end_time = time.time() + duration
        frame_count = 0

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Capture the first image
        first_img = window.capture_as_image()
        first_img_np = np.array(first_img)
        frame_path = os.path.join(save_path, f"frame_{frame_count:04d}.png")
        cv2.imwrite(frame_path, cv2.cvtColor(first_img_np, cv2.COLOR_BGR2RGB))
        frame_count += 1

        while time.time() < end_time:
            # Capture the next image
            next_img = window.capture_as_image()
            next_img_np = np.array(next_img)
            
            # Calculate the difference between the first image and the next image
            diff_percentage = calculate_difference(first_img_np, next_img_np)
            
            if diff_percentage > 40:
                # Save the frame as an image file
                frame_path = os.path.join(save_path, f"frame_{frame_count:04d}.png")
                cv2.imwrite(frame_path, cv2.cvtColor(next_img_np, cv2.COLOR_BGR2RGB))
                
                # Update the first image to the current image
                first_img_np = next_img_np
                frame_count += 1

            time.sleep(frame_time)

        print(f"Recording saved to {save_path}")

    except Exception as e:
        print(f"Failed to record window: {e}")

if __name__ == "__main__":
    windows = list_windows()
    window = choose_window(windows)
    if window:
        record_window(window, "recorded_images")
