# LogMonitor

`LogMonitor` allows users to get Sublime Text to automatically reload files in the editor every few seconds. This is particularly useful for monitoring log files that get continuously updated, even while the editor is not in focus.

## Use Case

Perfect for monitoring real-time logs on a secondary monitor while running fullscreen applications. By default, Sublime Text only reloads files when its window comes back into focus. `LogMonitor` eliminates this limitation by providing continuous file monitoring.

## Features

- **Log Syntax Support**: Enables auto-refresh for files using the project-defined `Log` syntax (*.log and *.logs files are automatically recognized)
- **Intelligent Cursor Management**: Automatically follows new content when cursor is at file end, preserves reading position when cursor is elsewhere

## Usage

### Automatic Log Monitoring

`LogMonitor` automatically enables for files using the **Log syntax**:

- **Automatic Syntax Recognition**: Files with *.log and *.logs extensions are automatically recognized as Log syntax
- **Manual Syntax Change**: Or manually set syntax to "Log" (View → Syntax → Log)
- **Smart Behavior**
   - If cursor is at the end of file → automatically scrolls to show new content
   - If cursor is in the middle → preserves your reading position

### Manual Control

From the command palette:

- **Enable Monitoring**: Start monitoring the current file
- **Disable Monitoring**: Stop monitoring the current file

## Configuration

Create `LogMonitor.sublime-settings` in your User package folder:

```json
{   
    "auto_refresh_rate": 5,
    "cursor_end_threshold": 30
}
```

- `auto_refresh_rate`: Refresh interval in seconds (default: 5)
- `cursor_end_threshold`: Number of lines from end to consider cursor "at end" for auto-scrolling (default: 30)

### Log Syntax Recognition

The included `Log.sublime-syntax` file defines `file_extensions: [log, logs]`, which automatically applies Log syntax to *.log and *.logs files when opened in Sublime Text. This enables seamless auto-refresh functionality without manual syntax configuration.

## Credits

This project is based on [AutoRefresh](https://github.com/Waterflames/AutoRefresh) by Waterflames.
Modifications have been made to focus on log file monitoring with intelligent cursor management.
