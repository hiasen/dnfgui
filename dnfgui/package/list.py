import dnf

from gi.repository import Gtk, GObject


class PackageList(GObject.Object, Gtk.TreeModel):
    attributes = dir(dnf.package.Package)
    attr_to_index = {attr: index for index, attr in enumerate(attributes)}

    @classmethod
    def get_index_of_attribute(cls, attr):
        return cls.attr_to_index[attr]
    
    def __init__(self, packages):
        self.packages = packages
        GObject.GObject.__init__(self)

    def get_package(self, path):
        return self.packages[path[0]]

    # Implementation of virtual methods

    def do_get_column_type(self, column):
        return str

    def do_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY

    def do_get_iter(self, path):
        index, *_ = path.get_indices()
        if index < len(self.packages):
            it = Gtk.TreeIter()
            it.user_data = index
            return (True, it)
        else:
            return (False, None)

    def do_get_path(self, it):
        if it.user_data is not None:
            path = Gtk.TreePath((it.user_data,))
            return path
        else:
            return None

    def do_get_value(self, it, column):
        package = self.packages[it.user_data]
        attribute = self.attributes[column]
        return str(getattr(package, attribute))

    def do_get_n_columns(self):
        return len(self.attributes)

    def do_iter_next(self, it):
        if it.user_data is not None and it.user_data < len(self.packages) - 1:
            it.user_data += 1
            return (True, it)
        else:
            return (False, None)

