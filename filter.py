import os
import time
import threading
import psutil
import asyncio
import geocoder
import pyautogui
import python_weather
from pathlib import Path
from pycaw.pycaw import AudioUtilities
from winotify import Notification
from comtypes import COMMETHOD, GUID, IUnknown
from datetime import datetime
from datetime import date

original_message = None
stopwatch_started_at = None

# ----------------------------------------------------------------------------------- # 
# --------------------------------- Functions --------------------------------------- # 
# ----------------------------------------------------------------------------------- # 

def set_master_volume(percent: int) -> str:
    speakers = AudioUtilities.GetSpeakers()
    speakers.EndpointVolume.SetMasterVolumeLevelScalar(percent / 100, None)
    return f"Volume set to {percent}%."

def show_notification(title: str, message: str) -> None:
    icon_path = Path(__file__).resolve().parent / "img" / "window.ico"
    Notification(
        app_id="Anna",
        title=title,
        msg=message,
        icon=str(icon_path),
    ).show()

def finish_timer(minutes: int) -> None:
    show_notification("Timer finished", f"Your {minutes}-minute timer has ended.")

def finish_reminder(name: str) -> None:
    show_notification("Reminder", name)

def get_curr_country():
    g = geocoder.ip('me')

    if g.ok:
        return g.country

def get_curr_city():
    g = geocoder.ip('me')

    if g.ok:
        return g.city

def get_battery_status():
    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery status unavailable."

    status = "Plugged in" if battery.power_plugged else "On battery"
    time_left = battery.secsleft
    unknown_time_values = {
        psutil.POWER_TIME_UNKNOWN,
        psutil.POWER_TIME_UNLIMITED,
        0xFFFFFFFF,
    }

    if time_left in unknown_time_values or time_left < 0:
        time_remaining = "unavailable"
    else:
        hours, remainder = divmod(time_left, 3600)
        minutes = remainder // 60
        time_remaining = f"{hours}h {minutes}m"

    estimate_label = "Time to full" if battery.power_plugged else "Time until battery dies"
    return (
        f"Battery: {battery.percent:.0f}%\n"
        f"Status: {status}\n"
        f"{estimate_label}: {time_remaining}"
    )

    

async def fetch_weather(city_name: str) -> dict:
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        weather = await client.get(city_name)

        return {
            "temp" : weather.temperature,
            "description" : weather.description
        }

def process_message(msg):
    global stopwatch_started_at

    original_message = msg.lower()

    if "run command" in original_message:
        command_start = original_message.index("run command") + len("run command")
        command_text = msg[command_start:].strip()
        command = command_text.lower()

# ---------------------------------------------------------------------------------------------------------- #
#                       Simple Commands (take no arguements)
# ---------------------------------------------------------------------------------------------------------- #


        if command == "time":
            now = datetime.now()
            return now.strftime("%H:%M:%S")

        if command == "date":
            return date.today().strftime("%d/%m/%Y")

        if command == "weather":
            city = get_curr_city()
            country = get_curr_country()
            weather_data = asyncio.run(fetch_weather(city))

            curr_weather = f"{weather_data['temp']}°C, {weather_data['description']}, {city} {country}"

            return curr_weather
               
        if command == "screenshot":
            folder_path = os.path.join(os.path.expanduser("~"), "Pictures", "screenshots")
            os.makedirs(folder_path, exist_ok=True)
            now = datetime.now()

            date_str = date.today().strftime("%d-%m-%Y")
            time_str = now.strftime("%H%M%S")

            filename = f"screenshot-{date_str}-{time_str}.png"
            full_path = os.path.join(folder_path, filename)

            pyautogui.screenshot(full_path)
            return f"Screenshot taken. Saved as {full_path}"
        
        if command == "mute":
            pyautogui.press("volumemute")
            return "Muted"
        
        if command == "pause":
            pyautogui.press("playpause")
            return "Paused"

        if command == "skip":
            pyautogui.press("nexttrack")
            return "Skipped."
        
        if command == "stopwatch":
            if stopwatch_started_at is None:
                stopwatch_started_at = time.perf_counter()
                return "Stopwatch started."

            elapsed_seconds = time.perf_counter() - stopwatch_started_at
            stopwatch_started_at = None
            hours, remainder = divmod(elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return (
                f"Stopwatch stopped. Total time: "
                f"{int(hours):02}:{int(minutes):02}:{seconds:06.3f}"
            )
            
        if command == "battery":
            return get_battery_status()

# ---------------------------------------------------------------------------------------------------------- #
#                       Complex Commands (take multiple arguements)
# ---------------------------------------------------------------------------------------------------------- #

        words = command.split()

        if len(words) >= 4 and words[0] == "reminder":
            raw_words = command_text.split()
            reminder_name = " ".join(raw_words[1:-2]).strip()
            try:
                reminder_time = datetime.strptime(
                    f"{words[-2]} {words[-1]}",
                    "%d/%m/%Y %H:%M",
                )
            except ValueError:
                return "Use the format: reminder <name> DD/MM/YYYY HH:MM (24-hour)."

            delay_seconds = (reminder_time - datetime.now()).total_seconds()
            if delay_seconds <= 0:
                return "Reminder date and time must be in the future."

            timer = threading.Timer(
                delay_seconds,
                finish_reminder,
                args=(reminder_name,),
            )
            timer.daemon = True
            timer.start()
            return f"Reminder set for {reminder_name} at {words[-2]} {words[-1]}."

        if len(words) == 2 and words[0] == "timer":
            try:
                minutes = int(words[1])
            except ValueError:
                return "Please provide a whole number of minutes for the timer."

            if minutes < 1:
                return "Timer duration must be at least 1 minute."

            timer = threading.Timer(minutes * 60, finish_timer, args=(minutes,))
            timer.daemon = True
            timer.start()
            return f"Timer set for {minutes} minute(s)."

        if len(words) == 2 and words[0] == "volume":
            try:
                percent = int(words[1])
            except ValueError:
                return "Please provide a whole-number volume percentage from 0 to 100."

            if not 0 <= percent <= 100:
                return "Volume percentage must be between 0 and 100."

            return set_master_volume(percent)
    
    return msg 

