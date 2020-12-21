
from gi.repository import Gtk, GObject

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


class PackageDetail(Gtk.Grid):
    def __init__(self, package):
        Gtk.Grid.__init__(self, column_spacing=10)
        for row, attribute in enumerate(attributes):
            key = Gtk.Label(label=attribute)
            key.set_halign(Gtk.Align.START)
            value = Gtk.Label(label=getattr(package, attribute))
            value.set_halign(Gtk.Align.START)
            self.attach(key, 0, row, 1, 1)
            self.attach(value, 1, row, 1, 1)