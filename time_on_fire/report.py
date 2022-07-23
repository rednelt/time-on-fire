# =======================================================
# Helper functions for retrieving data from the database
# =======================================================

import sqlite3
import tabulate
import time
import datetime


# Returns a ready to print table, based on provided
# date range and mode
def report(date_range, mode):
    conn = sqlite3.connect("activities.db")
    cursor = conn.cursor()

    table_headers = {
        "total": ["Name", "Total screen time"],
        "avg": ["Name", "Average screen time"],
        "raw": ["Id", "Date", "Process name", "Start", "End"]
    }

    # Ensure the table is created
    cursor.execute("CREATE TABLE IF NOT EXISTS activities ("
                   " id INTEGER PRIMARY KEY,"
                   " date TEXT NOT NULL,"
                   " process_name TEXT NOT NULL,"
                   " start INTEGER NOT NULL,"
                   " end INTEGER NOT NULL)")

    if mode == "total":
        # Total time in seconds per process name in range
        # If we just sum up all screen time in range (end - start), SQLite will cap it at 24 hours
        # because it treats the screen time as datetime.
        total = list(cursor.execute("SELECT process_name, "
                                    "SUM(STRFTIME('%s', end) - STRFTIME('%s', start))"
                                    "FROM activities "
                                    "WHERE date BETWEEN ? AND ?  "
                                    "GROUP BY process_name "
                                    "ORDER BY "
                                    "SUM(STRFTIME('%s', end) - STRFTIME('%s', start)) DESC",
                                    (date_range[0], date_range[1])))

        result = []
        for row in total:
            result.append((row[0], datetime.timedelta(seconds=int(row[1]))))

    elif mode == "avg":
        # Get total time in seconds per process name in range, then divide them
        # by a number of days during which the user had activity.
        # It's easier to postprocess the results, than doing this in pure SQL.
        total = list(cursor.execute("SELECT process_name, "
                                    "SUM(STRFTIME('%s', end) - STRFTIME('%s', start)) "
                                    "FROM activities "
                                    "WHERE date BETWEEN ? AND ? AND"
                                    "GROUP BY process_name "
                                    "ORDER BY "
                                    "SUM(STRFTIME('%s', end) - STRFTIME('%s', start)) DESC",
                                    (date_range[0], date_range[1])))

        # Get number of days to average on
        days = int(list(cursor.execute("SELECT COUNT(DISTINCT date) FROM activities WHERE date BETWEEN ? AND ?",
                                       (date_range[0], date_range[1])))[0][0])

        # Calculate the average time per process name and convert to HH:MM:SS
        result = []
        for row in total:
            result.append((row[0], datetime.timedelta(seconds=int(row[1]) // days))) 

    elif mode == "raw":
        # Pull out the raw records, nothing fancy
        result = cursor.execute("SELECT * "
                                "FROM activities "
                                "WHERE date BETWEEN ? AND ? AND process_name = 'EscapeFromTarkov.exe'",
                                (date_range[0], date_range[1]))

        table = tabulate.tabulate(result, tablefmt="fancy_grid", headers=["Id", "Date", "Process name", "Start", "End"])
        return table
    else:
        raise Exception("Invalid report mode:", mode)

    if result:
        # Format the data with tabulate
        table = tabulate.tabulate(result, tablefmt="fancy_grid", headers=table_headers[mode])
        return table
    else:
        return None
