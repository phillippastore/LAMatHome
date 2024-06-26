import re
import time
import ctypes
import logging
import subprocess
import platform
from utils.helpers import log_disabled_integration
from utils.config import config

############################
#      ComputerVolume      #
############################

def is_mac():
    return platform.system() == "Darwin"

def ComputerVolume(title):
    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()
    words = title_cleaned.split()
    if len(words) < 3:
        logging.error(f"Invalid prompt format '{title_cleaned}' for Computer Volume command.")
        return

    volume_word = words[2]

    if is_mac():
        if volume_word == "mute":
            subprocess.run(["osascript", "-e", "set volume with output muted"])
            logging.info("Muted the volume")
        elif volume_word == "unmute":
            subprocess.run(["osascript", "-e", "set volume without output muted"])
            logging.info("Unmuted the volume")
        elif volume_word == "up":
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10) --100%"])
            logging.info("Increased volume")
        elif volume_word == "down":
            subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10) --100%"])
            logging.info("Decreased volume")
        else:
            try:
                volume_value = int(volume_word)
                if volume_value < 0 or volume_value > 100:
                    raise ValueError
                subprocess.run(["osascript", "-e", f"set volume output volume {volume_value} --100%"])
                logging.info(f"Set volume to {volume_value}%")
            except ValueError:
                logging.error(f"Invalid volume value: {volume_word}. Must be an integer between 0 and 100.")
    else:
        if volume_word == "mute":
            try:
                ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
                logging.info("Muted the volume")
            except Exception as e:
                logging.error(f"Failed to mute volume: {e}")
            return

        if volume_word == "unmute":
            try:
                ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
                logging.info("Unmuted the volume")
            except Exception as e:
                logging.error(f"Failed to unmute volume: {e}")
            return

        if volume_word == "up":
            try:
                for _ in range(config['vol_up_step_value']):
                    ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                    ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
                logging.info(f"Increased volume by {config['vol_up_step_value']} steps")
            except Exception as e:
                logging.error(f"Failed to increase volume: {e}")
            return

        if volume_word == "down":
            try:
                for _ in range(config['vol_down_step_value']):
                    ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                    ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
                logging.info(f"Decreased volume by {config['vol_down_step_value']} steps")
            except Exception as e:
                logging.error(f"Failed to decrease volume: {e}")
            return

        try:
            volume_value = int(volume_word)
            if volume_value < 0 or volume_value > 100:
                raise ValueError
        except ValueError:
            logging.error(f"Invalid volume value: {volume_word}. Must be an integer between 0 and 100.")
            return

        try:
            for _ in range(50):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            for _ in range(volume_value // 2):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            logging.info(f"Set volume to {volume_value}%")
        except Exception as e:
            logging.error(f"Failed to set volume: {e}")

###############################
#        ComputerRun          #
###############################

computerrun_isenabled = True

def ComputerRun(title):

    title_cleaned = re.sub(r'[^\w\s]', '', title).lower()
    words = title_cleaned.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Run command.")
        return

    command = " ".join(words[2:])
    if is_mac():
        try:
            subprocess.run(['open', '-a', f'{command}'])
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke return'])
            logging.info(f"Executed command: {command}")
        except Exception as e:
            logging.error(f"Failed to execute command: {e}")
    else:
        try:
            # Press Windows key
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
            time.sleep(0.1)
            ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
            time.sleep(0.1)

            # Type the command
            for char in command:
                vk = ctypes.windll.user32.VkKeyScanW(ord(char))
                ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
                ctypes.windll.user32.keybd_event(vk, 0, 2, 0)
                time.sleep(0.05)

            # Press Enter
            ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)
            logging.info(f"Executed command: {command}")
        except Exception as e:
            logging.error(f"Failed to execute command: {e}")

#################################
#        ComputerMedia          #
#################################

computermedia_isenabled = True

def ComputerMedia(title):

    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Media command.")
        return

    action = words[2]

    if is_mac():
        try:
            if action == "next":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 124 using {command down}'])
                logging.info("Skipped to the next song")
            elif action == "back":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 123 using {command down}'])
                logging.info("Skipped to the previous song")
            elif action == "play" or action == "pause":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 49'])
                logging.info("Play/Pause the current song")
            else:
                logging.error("Invalid prompt format for Computer Media command.")
        except Exception as e:
            logging.error(f"Failed to execute media command: {e}")
    else:
        try:
            if action == "next":
                ctypes.windll.user32.keybd_event(0xB0, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xB0, 0, 2, 0)  # key up event
                logging.info("Skipped to the next song")
            elif action == "back":
                ctypes.windll.user32.keybd_event(0xB1, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xB1, 0, 2, 0)  # key up event
                logging.info("Skipped to the previous song")
            elif action == "play" or action == "pause":
                ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xB3, 0, 2, 0)  # key up event
                logging.info("Play/Pause the current song")
            else:
                logging.error("Invalid prompt format for Computer Media command.")
        except Exception as e:
            logging.error(f"Failed to execute media command: {e}")

#################################
#        ComputerPower          #
#################################

def ComputerPower(title):
    words = title.split()
    if len(words) < 3:
        logging.error("Invalid prompt format for Computer Power command.")
        return
    
    action = words[2].lower()
    logging.info(f"Action identified: {action}")

    if is_mac():
        try:
            if action == "lock":
                logging.info("Locking Mac...")
                subprocess.run(['osascript', '-e', 'tell application "System Events" to keystroke "q" using {control down, command down}'])

            elif action == "sleep":
                logging.info("Putting Mac to sleep...")
                subprocess.run(['osascript', '-e', 'tell application "System Events" to sleep'])

            elif action == "restart":
                logging.info("Restarting Mac...")
                subprocess.run(['osascript', '-e', 'tell application "System Events" to restart'])

            elif action == "shutdown":
                logging.info("Shutting down Mac...")
                subprocess.run(['osascript', '-e', 'tell application "System Events" to shut down'])
            else:
                logging.error(f"Unknown action: {action}")
        except Exception as e:
            logging.error(f"Failed to execute Mac command: {e}")

    else:
        try:
            if action == "lock":
                logging.info("Locking computer...")
                ctypes.windll.user32.LockWorkStation()

            elif action == "sleep":
                logging.info("Putting computer to sleep...")
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # win key down
                ctypes.windll.user32.keybd_event(0x58, 0, 0, 0)  # x key down
                ctypes.windll.user32.keybd_event(0x58, 0, 2, 0)  # x key up
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # win key up
                time.sleep(0.3)
                ctypes.windll.user32.keybd_event(0x55, 0, 0, 0)  # u key down
                ctypes.windll.user32.keybd_event(0x55, 0, 2, 0)  # u key up
                time.sleep(0.3)
                ctypes.windll.user32.keybd_event(0x53, 0, 0, 0)  # s key down
                ctypes.windll.user32.keybd_event(0x53, 0, 2, 0)  # s key up

            elif action == "restart":
                logging.info("Restarting computer...")
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # win key down
                ctypes.windll.user32.keybd_event(0x58, 0, 0, 0)  # x key down
                ctypes.windll.user32.keybd_event(0x58, 0, 2, 0)  # x key up
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # win key up
                ctypes.windll.user32.keybd_event(0x55, 0, 0, 0)  # u key down
                ctypes.windll.user32.keybd_event(0x55, 0, 2, 0)  # u key up
                ctypes.windll.user32.keybd_event(0x52, 0, 0, 0)  # r key down
                ctypes.windll.user32.keybd_event(0x52, 0, 2, 0)  # r key up

            elif action == "shutdown":
                logging.info("Shutting down computer...")
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # win key down
                ctypes.windll.user32.keybd_event(0x58, 0, 0, 0)  # x key down
                ctypes.windll.user32.keybd_event(0x58, 0, 2, 0)  # x key up
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # win key up
                ctypes.windll.user32.keybd_event(0x55, 0, 0, 0)  # u key down
                ctypes.windll.user32.keybd_event(0x55, 0, 2, 0)  # u key up
                ctypes.windll.user32.keybd_event(0x55, 0, 0, 0)  # u key down
                ctypes.windll.user32.keybd_event(0x55, 0, 2, 0)  # u key up

            else:
                logging.error(f"Unknown action: {action}")

        except Exception as e:
            logging.error(f"Failed to execute Windows command: {e}")