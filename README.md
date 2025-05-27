# AutoRefresh
Auto Refresh allows users to get Sublime text to reload files in the editor every x seconds (default 3 seconds)
This is useful for monitoring logs which get continuously edited, even while the editor is not in focus.

For example: You are running a fullscreen application and want to view the applications log on a different monitor.
By default, Sublime text will only reload the file once its window comes back into focus. 
AutoRefresh can be used here to automatically reload the file, without having to switch windows.

Usage:
From the commmand palette, use Enable AutoRefresh to enable. Similarly, use Disable AutoRefresh to stop the plugin.
Use "Autorefresh: Remember the current setting for this file" to automatically enable AutoRefresh when a file is opened.
To change the interval at which the file is refreshed: create a settings file called AutoRefresh.sublime-settings and set the setting auto_refresh_rate to how many seconds long you want the interval to be.


## File-based AutoRefresh

AutoRefresh supports two types of automatic file monitoring via the configuration in `Auto Refresh.sublime-settings` file:

- **File Name Based**: Configure `files_with_auto_refresh_enabled_on_load` with file paths. These specific files will auto-refresh when opened.

- **File Type Based**: Configure `file_types_auto_refresh` with file extensions like `[".log"]`. All matching file types will auto-refresh when opened.
