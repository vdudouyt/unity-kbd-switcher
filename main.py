from gi.repository import Gtk, Gio
from gi.repository import Keybinder
from internals import Layout, IMELayout, Circulate
import os, signal, string, internals

class Example(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
		Keybinder.init()

		# Initializing GSettings
		self.source_settings = Gio.Settings.new('org.gnome.desktop.input-sources')
		self.source_settings.connect("changed::current", self.on_current_changed)
		self.source_settings.connect("changed::sources", self.on_sources_changed)

		# Loading config
		rc = "%s/.kbdrc" % os.getenv("HOME")
		if not os.path.isfile(rc):
			self.generate_default_rc(rc)
		keymap = {}
		execfile(rc)
		self.keymap = keymap

		self.current_layout = None
		self.on_sources_changed(None, None)
		self.on_current_changed(None, None)

		# Binding global hotkeys
		for key in self.keymap.keys():
			print "Binding %s" % key
			if not Keybinder.bind(key, self.on_global_key_activated, None):
				self.show_message("Could not bind '%s'" % key)
		
		# Usual Gtk Stuff
		self.connect("destroy", Gtk.main_quit)
		self.connect("delete_event", Gtk.main_quit)
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		internals.app = self
		Gtk.main()

	def show_message(self, msg):
		dialog = Gtk.MessageDialog(self, 0,
				Gtk.MessageType.ERROR, Gtk.ButtonsType.CANCEL,
				msg)
		dialog.run()
		dialog.destroy()
	
	def generate_default_rc(self, path):
		language_codes = map(lambda (subsystem, language_code) : language_code, self.sources)
		with open(path, "w") as file:
			file.write("keymap['Caps_Lock'] = Circulate(%s)\n" % self.generate_strings_list(language_codes))
	
	def generate_strings_list(self, components):
		return string.join(map(lambda t: "'" + t + "'", components), ", ")
	
	def set_language(self, language_code):
		self.source_settings.set_uint('current', self.language_codes.index(language_code))
	
	def on_global_key_activated(self, keystr, user_data):
		todo = self.keymap[keystr]
		if type(todo) == str:
			todo = SetLayout(todo)
		todo.run()
	
	def on_current_changed(self, settings, name):
		if self.current_layout:
			self.previous_layout = self.current_layout
		self.current = self.source_settings.get_uint('current')
		self.current_language_code = self.language_codes[self.current]
		self.current_layout = internals.language_code_to_layout[self.current_language_code]
		self.current_grouping = internals.language_code_to_grouping[self.current_language_code]
		# current_grouping may contain childs, need to notify that the language changed
		if self.current_layout != self.current_grouping:
			self.current_grouping.set_language(self.current_language_code)
	
	def on_sources_changed(self, settings, name):
		self.sources = self.source_settings.get_value('sources')
		self.language_codes = map(lambda (subsystem, language_code) : language_code, self.sources)

if __name__ == "__main__":
	Example()
