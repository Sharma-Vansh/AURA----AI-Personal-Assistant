import os
import datetime
import webbrowser
import subprocess
import platform
import screen_brightness_control as sbc

OS_NAME = platform.system().lower()


# ============================================================
#  VOLUME CONTROL  (Requires nircmd.exe in project folder)
# ============================================================

def increase_volume():
    os.system("nircmd.exe changesysvolume 5000")
    return "Volume 10% badha diya hai."

def decrease_volume():
    os.system("nircmd.exe changesysvolume -5000")
    return "Volume 10% kam kar diya hai."

def mute_volume():
    os.system("nircmd.exe mutesysvolume 1")
    return "Volume mute kar diya hai."

def unmute_volume():
    os.system("nircmd.exe mutesysvolume 0")
    return "Volume unmute kar diya hai."


# ============================================================
#  BRIGHTNESS CONTROL
# ============================================================

def increase_brightness():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(min(100, current + 10))
    return "Brightness 10% badha di hai."

def decrease_brightness():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(max(0, current - 10))
    return "Brightness 10% kam kar di hai."


# ============================================================
#  BASIC APPS (Force Chrome for Windows)
# ============================================================

def force_open(url):
    try:
        os.system(f'start chrome "{url}"')
        return True
    except:
        return False


def open_notepad():
    try:
        subprocess.Popen("notepad.exe")
        return True
    except:
        return False

def open_chrome():
    return force_open("https://www.google.com")

def open_youtube():
    return force_open("https://www.youtube.com")

def open_whatsapp_web():
    return force_open("https://web.whatsapp.com")

def open_facebook():
    return force_open("https://facebook.com")

def open_spotify():
    return force_open("https://open.spotify.com")

def open_colab():
    return force_open("https://colab.research.google.com")

def open_lighting():
    return force_open("https://www.google.com/search?q=RGB+PC+lighting")


def open_file_explorer():
    os.system("start explorer")
    return True


# ============================================================
#  TIME / DATE
# ============================================================

def say_time():
    now = datetime.datetime.now()
    return now.strftime("Abhi %I:%M %p baj rahe hain.")

def say_time_detailed():
    now = datetime.datetime.now()
    return now.strftime("Abhi %I bajkar %M minute %p hai.")

def say_date():
    today = datetime.date.today()
    return today.strftime("Aaj ki date %d-%m-%Y hai.")


# ============================================================
#  MAIN COMMAND HANDLER
# ============================================================

def handle_system_command(text: str):
    t = text.lower()

    # TIME DATE
    if "time" in t:
        return True, say_time()

    if "date" in t:
        return True, say_date()

    # Notepad
    if "notepad" in t:
        return True, "Notepad open kar diya hai." if open_notepad() else "Notepad nahi khula."

    # Chrome / Browser
    if "chrome" in t or "browser" in t:
        return True, "Chrome open kar diya hai." if open_chrome() else "Chrome nahi khula."

    # YouTube
    if "youtube" in t:
        open_youtube()
        return True, "YouTube open kar diya hai."

    # WhatsApp
    if "whatsapp" in t:
        open_whatsapp_web()
        return True, "WhatsApp Web open kar diya hai."

    # Facebook
    if "facebook" in t:
        open_facebook()
        return True, "Facebook open kar diya hai."

    # Spotify
    if "spotify" in t:
        open_spotify()
        return True, "Spotify open kar diya hai."

    # Colab
    if "colab" in t or "google colab" in t:
        open_colab()
        return True, "Google Colab open kar diya hai."

    # Lighting
    if "lighting" in t or "rgb" in t:
        open_lighting()
        return True, "Lighting settings open kar diye."

    # File Explorer
    if "file explorer" in t or "my computer" in t:
        open_file_explorer()
        return True, "File Explorer open kar diya hai."

    # VOLUME
    if "increase volume" in t or "volume badhao" in t:
        return True, increase_volume()

    if "decrease volume" in t or "volume kam karo" in t:
        return True, decrease_volume()

    if "mute" in t:
        return True, mute_volume()

    if "unmute" in t:
        return True, unmute_volume()

    # BRIGHTNESS
    if "increase brightness" in t or "brightness badhao" in t:
        return True, increase_brightness()

    if "decrease brightness" in t or "brightness kam karo" in t:
        return True, decrease_brightness()

    return False, None
