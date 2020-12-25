#!/usr/bin/env python
import gi
gi.require_version("Gtk", "3.0")

import dnfgui.app

app = dnfgui.app.App()
app.run()
