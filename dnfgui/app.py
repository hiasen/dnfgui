
import dnf
import threading
from gi.repository import Gtk, GObject

from .package import PackageList, PackageListView, PackageDetail


class App(Gtk.Application):
    def __init__(self, *args):
        super().__init__(*args)
        self.base = dnf.Base()

        thread = threading.Thread(target=self.initialize_dnf)
        thread.daemon = True
        thread.start()

    def do_activate(self):
        win = AppWindow(application=self)
        win.show_all()

    def initialize_dnf(self):
        print("reading repos")
        self.base.read_all_repos()
        print("filling sack")
        self.base.fill_sack()
        print("filled sack")

    def simple_query(self, text):
        subject = dnf.subject.Subject(text)
        query = subject.get_best_query(self.base.sack)
        return query.run()


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, application):
        super().__init__(application=application, title="dnf")
        self.props.default_width = 800
        self.props.default_height = 600

        self.tree = PackageListView([])
        self.tree.connect("row-activated", self.on_package_click)
        self.tree.props.activate_on_single_click = True

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.add(self.tree)

        entry = Gtk.Entry()
        entry.connect("activate", self.on_entry_activate)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.add(entry)
        box.add(scrolled_window)

        self.package_detail = PackageDetail()
        box.add(self.package_detail)

        self.add(box)

    def on_entry_activate(self, entry):
        packages = self.props.application.simple_query(entry.get_text())
        model = PackageList(packages)
        self.tree.set_model(model)

    def on_package_click(self, tree_view, path, column):
        model = tree_view.get_model()
        package = model.get_package(path)
        self.package_detail.set_package(package)
