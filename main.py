from gi.repository import Gtk, Gio, GLib
from gi.repository import Keybinder
from internals import Layout, IMELayout, Circulate
import os, signal, string, internals

class Example(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
		Keybinder.init()

		# Deactivating WM keybindings
		keybindings = Gio.Settings.new('org.gnome.desktop.wm.keybindings')
		wm_hotkey = lambda t: keybindings.get_value(t)[0]
		if wm_hotkey('switch-input-source') or wm_hotkey('switch-input-source-backward'):
			self.show_message("Unity-Kbd-Switcher is going to deactivate the following WM keybindings\n"
				+ "You can set them later in settings if you'll decide to discontinue using.\n"
				+ "\n"
				+ "switch-input-source: " + wm_hotkey('switch-input-source') + "\n"
				+ "switch-input-source-backward: " + wm_hotkey('switch-input-source-backward') + "\n")
			keybindings.set_value('switch-input-source', GLib.Variant('as', ['']))
			keybindings.set_value('switch-input-source-backward', GLib.Variant('as', ['']))

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
				Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
				msg)
		dialog.set_title('unity-kbd-switcher')
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

		# Check that all language_codes are known by system
		langs_cfg = internals.language_code_to_layout.keys()
		langs_system = self.language_codes
		languages_not_found = [ lang for lang in langs_cfg if lang not in langs_system ]
		if len(languages_not_found):
			self.show_message("Couldn't find the following languages: " + string.join(languages_not_found, ", ") + "\n"
			+ "Please add in System Settings -> Text Entry -> Input sources.")

if __name__ == "__main__":
	Example()
