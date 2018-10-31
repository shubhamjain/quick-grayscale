import rumps, re, os

from pathlib import Path
from subprocess import Popen, PIPE, call

def is_grayscale():
    homepath = str(Path.home())
    ua_file = homepath + "/Library/Preferences/com.apple.universalaccess.plist"

    p = Popen(["plutil", "-p", ua_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)    
    output = p.communicate()[0]

    return re.findall(r"\"grayscale\" => ([0-9])", output.decode("utf8"))[0] == "1"

def quit_system_preferences():
    call(["osascript", "-e", """
        tell application "System Preferences"
            quit
        end tell"""])

def toggle_grayscale(menuItem):
    p = Popen(["osascript", "-e", """tell application "System Preferences"
        activate
        reveal anchor "Seeing_Display" of pane id "com.apple.preference.universalaccess"
        end tell
        delay .5
        tell application "System Events" to tell process "System Preferences"
            try
                click checkbox "Use grayscale" of group 1 of window "Accessibility"
            on error
                click checkbox "Use greyscale" of group 1 of window "Accessibility"
            end try
        end tell
        tell application "System Preferences"
            quit
        end tell"""
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    err = p.communicate()[1]

    if (not err):
        menuItem.state = not menuItem.state

    error_code = re.findall(r"([0-9]+)", err.decode("utf8"))[-1]

    if (error_code == "1728"):
        quit_system_preferences()
        rumps.alert(title="Permissions Required",
            message="Quick Grayscale needs accessibility permissions to modify the Grayscale display setting.\n\n" + 
                "Please enable them for the app" + 
                " by going to Security & Privacy > Privacy > Accessiblity (on the left pane) and allowing Quick Grayscale.")
    elif (error_code == "1743"):
        quit_system_preferences()
        rumps.alert(title="Permissions Required",
            message="Quick Grayscale needs System Events permission to configure System Preferences. " +
            "Please enable it by going Security & Privacy > Privacy > Automation (on the left pane) and clicking the" + 
                "'System Events' checkbox for the app.")

        
if __name__ == "__main__":
    app = rumps.App("Quick Grayscale", icon="./status-bar-logo.png")
    menuItem = rumps.MenuItem ("Enable Grayscale", callback=toggle_grayscale)
    menuItem.state = is_grayscale()

    app.menu = [
        menuItem
    ]
    app.run()