# =======================================================
# Provides the track() function, that tracks time spent
# on apps and saves it to activities.db
# =======================================================
import tabulate
import win32gui
import psutil
import win32process
import sqlite3
import datetime
import time
import signal

from .config import *


interrupted = False


def track(debug=False):

    # Returns the process name of the foreground window
    def get_active_window_process_name():
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        try:
            process_name = psutil.Process(pid[-1]).name()
            return process_name

        except (psutil.NoSuchProcess, ValueError, ProcessLookupError):
            return None

    # We'll count the activities to print them later. Feedback, you know.
    activity_count = 0

    # Connect the database
    conn = sqlite3.connect("activities.db")
    cursor = conn.cursor()

    # A signal handler. When the user hits Ctrl+C, the script will only
    # exit after the data is saved
    def signal_handler(signal, frame):
        global interrupted
        interrupted = True
        print("Stopping...")

    signal.signal(signal.SIGINT, signal_handler)

    # Ensure the table is created
    cursor.execute("CREATE TABLE IF NOT EXISTS activities ("
                   " id INTEGER PRIMARY KEY,"
                   " date TEXT NOT NULL,"
                   " process_name TEXT NOT NULL,"
                   " start INTEGER NOT NULL,"
                   " end INTEGER NOT NULL)")

    print("Recording...\nHit Ctrl+C to stop.")

    # This is to get the current process when the script has started
    process_name_1 = get_active_window_process_name()
    while not process_name_1 or process_name_1 in IGNORE_PROCESSES:
        process_name_1 = get_active_window_process_name()

    if debug:
        print(process_name_1)

    date = datetime.date.today().strftime("%Y-%m-%d")

    start = datetime.datetime.now().strftime("%H:%M:%S")

    # Poll for the current process name and detect when it changes
    while True:
        process_name_2 = get_active_window_process_name()
        while not process_name_2:
            process_name_2 = get_active_window_process_name()

        # If process changed, add the activity into database
        if process_name_1 != process_name_2 and process_name_2 not in IGNORE_PROCESSES:

            end = datetime.datetime.now().strftime("%H:%M:%S")

            if debug:
                print(f"{process_name_1} {start} -> {process_name_2} {end}")

            # Update database, commit changes
            cursor.execute("INSERT INTO activities (date, process_name, start, end) VALUES (?, ?, ?, ?)",
                           (date, process_name_1, start, end))
            conn.commit()

            process_name_1 = process_name_2
            start = end
            activity_count += 1

        # If the user hits Ctrl+C, save changes and abort the loop
        if interrupted:
            cursor.execute("INSERT INTO activities (date, process_name, start, end) VALUES (?, ?, ?, ?)",
                           (date, process_name_1, start, datetime.datetime.now().strftime("%H:%M:%S")))
            conn.commit()
            activity_count += 1
            print(f"Recording stopped, {activity_count} activities added into the database.")
            return 0

        time.sleep(POLLING_DELAY)


# For debugging purposes, if track.py is ran as a script
if __name__ == "__main__":
    track(debug=True)
    conn = sqlite3.connect("activities.db")
    cursor = conn.cursor()
    data = tabulate.tabulate(cursor.execute("SELECT * FROM activities WHERE date BETWEEN 3024-24-56 AND 2012-92-08"),
                             tablefmt="fancy_grid")
    print(data)
    cursor.close()
