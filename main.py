#!/usr/bin/env python
import gi
import dnf


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject
from dnfgui.package import PackageList, PackageListView, PackageDetail

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
        
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.add(entry)
        self.box.add(scrolled_window)

        self.add(self.box)
        self.package_detail = None

    def on_entry_activate(self, entry):
        subject = dnf.subject.Subject(entry.get_text())
        query = subject.get_best_query(base.sack)
        model = PackageList(query.run())
        self.tree.set_model(model)

    def on_package_click(self, tree_view, path, column):
        model = tree_view.get_model()
        package = model.get_package(path)

        if self.package_detail is not None:
            self.box.remove(self.package_detail)
        self.package_detail = PackageDetail(package)
        self.box.add(self.package_detail)
        self.box.show_all()

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()