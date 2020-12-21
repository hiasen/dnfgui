#!/usr/bin/env python
import gi
import dnf


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from dnfgui.packagelist import PackageList
from dnfgui.packagelistview import PackageListView

base = dnf.Base()
base.read_all_repos()
base.fill_sack()
assert base.sack


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        
        self.tree = PackageListView(base.sack.query().installed().run())
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.tree)

        entry = Gtk.Entry()
        entry.connect("activate", self.on_entry_activate)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.add(entry)
        box.add(scrolled_window)

        self.add(box)
    
    def on_entry_activate(self, entry):
        subject = dnf.subject.Subject(entry.get_text())
        query = subject.get_best_query(base.sack)
        model = PackageList(query.run())
        self.tree.set_model(model)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()