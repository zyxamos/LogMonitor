import threading
import time
import sublime, sublime_plugin

refreshThreads = {}

# Enables autorefresh for the specified view
def enable_autorefresh_for_view(view):
	settings = sublime.load_settings('LogMonitor.sublime-settings')
	refreshRate = settings.get('auto_refresh_rate')

	if refreshRate == None or not isinstance(refreshRate, (int, float)):
		print("Invalid auto_refresh_rate setting, using default 5")
		refreshRate = 5

	if refreshThreads.get(view.id()) is None or not refreshThreads.get(view.id()).enabled:
		refreshThreads[view.id()] = RefreshThread(view, refreshRate)
		refreshThreads[view.id()].start()

# Disables autorefresh for the specified view.
# Does nothing if autorefresh was already disabled
def disable_autorefresh_for_view(view):
	thread = refreshThreads.get(view.id())
	if thread is not None:
		thread.enabled = False
		# Clean up the thread reference
		refreshThreads.pop(view.id(), None)


# Commands
class EnableMonitoringCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		enable_autorefresh_for_view(self.view)

class DisableMonitoringCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		disable_autorefresh_for_view(self.view)


# Event handler for editor events
class SublimeEventHandler(sublime_plugin.EventListener):
	def on_pre_close(self, view):
		disable_autorefresh_for_view(view)
	
	def on_load_async(self, view):
		self.enable_auto_refresh_on_load(view)
	
	def on_activated_async(self, view):
		# Only check if no thread exists or thread is disabled
		thread = refreshThreads.get(view.id())
		if thread is None or not thread.enabled:
			self.enable_auto_refresh_on_load(view)
	
	def enable_auto_refresh_on_load(self, view):
		# Only enable auto-refresh for Log syntax files
		syntax = view.settings().get('syntax')
		if syntax == "Packages/LogMonitor/Log.sublime-syntax":
			enable_autorefresh_for_view(view)


# Threading class that continuously reloads a file
class RefreshThread(threading.Thread):
	def __init__(self, view, refreshRate):
		self.view = view
		self.enabled = True
		self.refreshRate = refreshRate
		threading.Thread.__init__(self)
	
	def run(self):
		while self.enabled:
			try:
				if not self.view.is_dirty():  # Don't reload if user made changes
					sublime.set_timeout(self.reload_and_goto_last_line, 1)
			except Exception as e:
				print("LogMonitor error: {msg}".format(msg=e))
				self.enabled = False
				break
			time.sleep(self.refreshRate)

	def is_cursor_at_end(self):
		"""Check if cursor is near the end of file (within 3 lines)"""
		if not self.view.sel():
			return False
		
		cursor_row = self.view.rowcol(self.view.sel()[0].begin())[0]
		total_rows = self.view.rowcol(self.view.size())[0]
		
		# If cursor is within 3 lines of the end, consider it "at end"
		return (total_rows - cursor_row) <= 3

	def reload_and_goto_last_line(self):
		"""Reload file and go to last line only if cursor was at end"""
		should_goto_last_line = self.is_cursor_at_end()
		
		# Reload file
		self.view.run_command('revert')
		
		# If cursor was at end before reload, move to new end
		if should_goto_last_line:
			sublime.set_timeout(self.goto_last_line, 10)

	def goto_last_line(self):
		"""Move cursor to the last line of the file"""
		if not self.view.is_loading():
			self.view.run_command("move_to", {"to": "eof", "extend": False})
		else:
			# Wait for file to finish loading
			sublime.set_timeout(self.goto_last_line, 10)
