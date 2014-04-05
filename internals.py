import os

app = None
language_code_to_layout = {}
language_code_to_grouping = {}

class Circulate():
	"Cycle between a several layouts"
	def __init__(self, *args):
		self.subset = map(to_layout, args)
		self.pos = 0
		for layout in self.subset:
			language_code_to_grouping[layout.language_code] = self
	
	def set_language(self, language_code):
		filtered = filter(lambda t: t.language_code == language_code, self.subset)
		self.pos = self.subset.index(filtered[0])

	def run(self):
		self.pos = (self.pos + 1) % len(self.subset)
		todo = self.subset[self.pos]
		todo.run()

class Layout():
	"Simply enforce the layout"
	def __init__(self, language_code):
		self.language_code = language_code
		language_code_to_layout[language_code] = self
		language_code_to_grouping[language_code] = self

	def run(self):
		app.set_language(self.language_code)

class IMELayout(Layout):
	def run(self):
		if app.current_layout == self:
			app.set_language(app.previous_layout.language_code)
		else:
			os.system("setxkbmap us") # Avoid bug
			app.set_language(self.language_code)

def to_layout(t):
	return Layout(t) if type(t) is str else t
