# time-on-fire
A simple activity tracker written in Python for Windows 10.

### Why? There are time trackers already.
I didn\'t find a **simple** time tracker for Windows. A lot of them are for teams/are paid/have a lot of features that I didn\'t need (like tracking time spent on projects, graphs, analytics, goals, grouping activities and so forth). Most of the time I just needed to check what I was doing today, or to see the average screen time of my apps this week. For these simple tasks, `time-on-fire` is much better suited, allowing me to do them in a single keystroke: `tof report` and `tof report 2022-07-10:2022-07-16 -m avg` respectively. It\'s deliberately crude and simple, containing only 3 commands (only one of which takes an argument and an option). If you want a GUI and more advanced features, check out [ActivityWatch](https://activitywatch.net/ "ActivityWatch"). It\'s crossplatform, free and open source.


## Quickstart
### Installation 💾
Execute
```
pip install time-on-fire
```
in your terminal, and wait till pip finishes the installation. (or `py -m pip install tof` if didn\'t work)

### Tracking 🔎
To start tracking your activities, execute `tof track`. Your activities (apps, foreground processes) are now being saved into a database.

Hit Ctrl+C when you\'re done. Just don\'t forget to stop recording before you turn off your computer, as the last activity won\'t be saved!

You can add a `--debug` flag when you execute the `track` command, to see the transitions between activities (e.g. `1.exe 11:00 -> 2.exe 12:00`)

You can clear the database with `tof clear_db`.
### Creating reports 📊
Use the `report` command to create reports of your activities.
#### Arguments:
### `date_range`
A date in `YYYY-MM-DD` format, or a range of dates in `YYYY-MM-DD|YYYY-MM-DD`  format.  Default is today.  

#### Options:
### `--mode`, `-m`
One of the three modes: `total`, `avg` and `raw`.
- `total` - Total screen time per process in range.
- `avg`- Average screen time per day per process in range.
- `raw` - Raw records (id, date, process name, start time, end time) in range.

Default is `total`.


#### Examples:
```
tof report
```
returns a table summarizing your today activity;
<br/>
```
tof report 2022-05-05|2022-05-18 -m avg
```
returns a table, containing the average screen time of each process per day, from
5th to 18th of May;
<br/>

```
tof report 2022-04-01 -m raw
```
returns raw database records that were made on 1st of April.

### Config ⚙️
Do you have some app that pops up when idling and messes up your records (a reminder or an alarm, a floating dock, any process that\'s sometimes or always in the foreground, but you don\'t want to track its screen time)?

Good news, you can configure `time-on-fire` to ignore these processes!
How to find the config:

Execute `pip show tof` (or `py--m pip show tof`) and look for a Location row. Go to this path.

Inside `site-packages` folder (where you just navigated) look for a folder named (or contains) `time-on-fire`, then navigate inside.

There will be a `time_on_fire` folder (inside of `time-on-fire`), inside of which you\'ll find `config.py`, our configuration file!
It looks like this (without comments):
``` python
POLLING_DELAY = 0.2
IGNORE_PROCESSES = ["ShellExperienceHost.exe", "mbamtray.exe", "ueli.exe", "explorer.exe"]
```
`POLLING_DELAY` is how fast the script polls for the current foreground process.
`IGNORE PROCESSES` is a list of processes that the script will ignore. 

### Notes
- If, for example, you switch from Chrome to desktop, it will still count as Chrome\'s screen time, because `explorer.exe` does not only pop up at desktop, but also when clicking the taskbar or just idling. I have no reliable way of knowing whether the user switched to desktop or it\'s popping by itself (it could last from 3 seconds to 15 minutes during testing). Let me know if you have a fix.
- The inner `time_on_fire` folder is written with underscores, because it\'s a package, and Python packages shouldn\'t have an underscore. The outer folder is a repository (either on GitHub or PyPI).

That\'s it. That\'s the documentation. It\'s that simple.