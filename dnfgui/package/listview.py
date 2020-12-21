
from gi.repository import Gtk, GObject
from .list import PackageList


class PackageListView(Gtk.TreeView):
    def __init__(self, packages):
        store = PackageList(packages)
        Gtk.TreeView.__init__(self, model=store)
        renderer = Gtk.CellRendererText()
        self.append_column(Gtk.TreeViewColumn("Name", renderer, text=PackageList.get_index_of_attribute("name")))
        self.append_column(Gtk.TreeViewColumn("evr", renderer, text=PackageList.get_index_of_attribute("evr")))
        self.append_column(Gtk.TreeViewColumn("Installed", renderer, text=PackageList.get_index_of_attribute("installed")))
        self.append_column(Gtk.TreeViewColumn("Repo", renderer, text=PackageList.get_index_of_attribute("reponame")))
