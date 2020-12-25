
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


class PackageDetail(Gtk.Bin):
    __gtype_name__ = "PackageDetail"

    def __init__(self, package=None):
        super().__init__()
        if package is not None:
            self.set_package(package)

    def set_package(self, package):
        if (child := self.get_child()) is not None:
            self.remove(child)

        grid = Gtk.Grid(column_spacing=10)
        for row, attribute in enumerate(attributes):
            key = Gtk.Label(label=attribute)
            key.set_halign(Gtk.Align.START)
            value = Gtk.Label(label=getattr(package, attribute))
            value.set_halign(Gtk.Align.START)
            grid.attach(key, 0, row, 1, 1)
            grid.attach(value, 1, row, 1, 1)
        self.add(grid)
        self.show_all()
