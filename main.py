#!/usr/bin/env python
import gi
import dnf


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from dnfgui.package import PackageList, PackageListView

base = dnf.Base()
base.read_all_repos()
base.fill_sack()
assert base.sack


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        
        self.tree = PackageListView([])
        self.tree.connect("row-activated", self.on_package_click)
        
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

    def on_package_click(self, tree_view, path, column):
        model = tree_view.get_model()
        package = model.get_package(path)
        attributes = [
            "name",
            "version",
            "release",
            "arch",
            "downloadsize",
            "sourcerpm",
            "reponame",
            "summary",
            "url",
            "license",
            "description",
        ]
        window = Gtk.Window(title=str(package))
        grid = Gtk.Grid(column_spacing=10)

        for row, attribute in enumerate(attributes):
            key = Gtk.Label(label=attribute)
            key.set_halign(Gtk.Align.START)
            value = Gtk.Label(label=getattr(package, attribute))
            value.set_halign(Gtk.Align.START)
            grid.attach(key, 0, row, 1, 1)
            grid.attach(value, 1, row, 1, 1)
        window.add(grid)
        window.show_all()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()