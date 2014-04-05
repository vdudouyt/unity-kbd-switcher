unity-kbd-switcher
==================

Alternative language switcher with sophisticated keybindings configuration

### ~/.kbdrc examples

1. Caps Lock circulates between English and Russian, Ctrl+Space switches to Japanese:
 
 ```nohighlight
 keymap['Caps_Lock'] = Circulate('us', 'ru')
 keymap['<Control>space'] = IMELayout('anthy')
 ```
 
2. Alt+&lt;1, 2, 3&gt; switches to English, Russian and Ukrainian correspondingly:
 
 ```nohighlight
 keymap['<Alt>1'] = 'en'
 keymap['<Alt>2'] = 'ru'
 keymap['<Alt>3'] = 'ua'
 ```

### Installation

1. Install a [DEB package](https://github.com/vdudouyt/unity-kbd-switcher/releases/)
2. Restart session
