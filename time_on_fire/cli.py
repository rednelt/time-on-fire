# =======================================================
# CLI interface for the app
# =======================================================
from datetime import date
import click
import sqlite3
import re
import sys

from .track import track
from .report import report


@click.group()
def cli():
    pass


@cli.command(name="track", help="Track your activities and save them into a database. ")
@click.option("--debug", is_flag=True, help="Print the transitions between processes (1.exe 11:00 -> 2.exe 12:00)")
def track_(debug):
    track(debug)


@cli.command(name="report", help="Create a report of your activities.")
@click.argument("date_range", default=f"{date.today()}:{date.today()}")
@click.option("--mode", "-m", default="total", type=click.Choice(["total", "avg", "raw"]),
              help="One of the three modes: total, avg and raw. Default is total.")
def report_(date_range, mode):  # _ to avoid name collision
    date_regex = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    date_range_regex = "^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\:\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

    # Validate the provided date
    if re.search(date_regex, date_range):
        # If given a single date, convert to a range
        date_range = [date_range, date_range]
    elif re.search(date_range_regex, date_range):
        # If given a range, split into a list
        date_range = date_range.split(":")
    else:
        print(f"Error: Invalid date (range) '{date_range}'."
              f" Please use one of the following formats: 'YYYY-MM-DD' or 'YYYY-MM-DD:YYYY-MM-DD'")
        sys.exit()

    # Print results
    print(f"Results for {':'.join(date_range) if date_range[0] != date_range[1] else date_range[0]} in {mode} mode:")
    result = report(date_range, mode)
    print(result if result else "No data. Looks like there are no activities in this range!")


@cli.command(name="clear_db", help="Clear the activity database.")
def clear_db():
    if click.confirm("Do you want to clear the database? You won't be able to restore it."):
        conn = sqlite3.connect("activities.db")
        cursor = conn.cursor()
        rows_count = int(list(cursor.execute("SELECT COUNT(id) FROM activities"))[0][0])
        cursor.execute("DROP TABLE activities")
        print(rows_count, "row(s) deleted succesfully.")
        conn.close()


if __name__ == '__main__':
    cli()
