unity-kbd-switcher
==================

Alternative language switcher with sophisticated hotkeys configuration

Note: this program will unset your default layout switch shortcut on startup. It's easy to set it back in System Preferences if you'll decide to discontinue using.

### Configuration examples

1. Caps Lock circulates between English and Russian, Ctrl+Space switches to Japanese/Anthy:
 
 ```nohighlight
 keymap['CAPS_LOCK'] = Circulate('en', 'ru')
 keymap['<Ctrl>Space'] = IBusLayout('ja')
 ```
 
2. Alt+&lt;1, 2, 3&gt; switches to English, Russian and Ukrainian correspondingly:
 
 ```nohighlight
 keymap['<Alt>1'] = 'en'
 keymap['<Alt>2'] = 'ru'
 keymap['<Alt>3'] = 'ua'
 ```
