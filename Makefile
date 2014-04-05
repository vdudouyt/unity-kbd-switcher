SHARE=$(DESTDIR)/usr/share/unity-kbd-switcher/
XDG_AUTOSTART=$(DESTDIR)/etc/xdg/autostart/
SOURCES=$(wildcard *.py)

install:
	mkdir -p $(SHARE)
	mkdir -p $(XDG_AUTOSTART)
	cp $(SOURCES) $(SHARE)
	cp autostart/unity-kbd-switcher.desktop $(XDG_AUTOSTART)
