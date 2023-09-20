## Dependencies

 * requests
 * pyinstaller (optionally)

## Setup

For better visuals of the notifications we recommend bundling the Notifier into an executable like this (byt first adjust the appPath in Notifier.pyw) `pyinstaller -i epic-games-icon.ico --onefile Notifier.pyw`. Use the executable in the `dist` folder and delete the rest.

Then you need to put a shortcut to the executable into the Windows Start menu by inserting the shortcut into `AppData\Roaming\Microsoft\Windows\Start Menu\Programs`

Then we recommend setting automatic running of the code. Do this in Windows Task scheduler.
