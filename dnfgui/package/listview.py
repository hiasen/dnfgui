
from gi.repository import Gtk, GObject
from .list import PackageList


class PackageListView(Gtk.TreeView):
    __gtype_name__ = "PackageListView"
    def __init__(self, packages=None):
        if packages is None:
            packages = []
        store = PackageList(packages)
        super().__init__(model=store)
        renderer = Gtk.CellRendererText()
        self.append_column(Gtk.TreeViewColumn("Name", renderer, text=PackageList.get_index_of_attribute("name")))
        self.append_column(Gtk.TreeViewColumn("evr", renderer, text=PackageList.get_index_of_attribute("evr")))
        self.append_column(Gtk.TreeViewColumn("Installed", renderer, text=PackageList.get_index_of_attribute("installed")))
        self.append_column(Gtk.TreeViewColumn("Repo", renderer, text=PackageList.get_index_of_attribute("reponame")))
