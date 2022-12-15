# How often the script will check if the process changed, in seconds
POLLING_DELAY = 0.2

# These processes randomly pop up when idling, the script will ignore
# them. You can add your own of similar nature (a reminder or an alarm,
# a floating dock, any process that's sometimes or always in the foreground,
# but you don't want to track its screen time)
IGNORE_PROCESSES = ["ShellExperienceHost.exe", "StartMenuExperienceHost.exe", "mbamtray.exe", "SearchApp.exe", "ueli.exe", "explorer.exe", "dwm.exe"]
