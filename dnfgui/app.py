
import dnf
import threading
from gi.repository import Gtk, GObject

from .package import PackageList, PackageListView, PackageDetail

import os

MAIN_UI_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "main.ui")

class App(Gtk.Application):
    def __init__(self, *args):
        super().__init__(*args)
        self.base = dnf.Base()

        thread = threading.Thread(target=self.initialize_dnf)
        thread.daemon = True
        thread.start()

    def do_activate(self):
        self.builder = Gtk.Builder.new_from_file(MAIN_UI_FILE)
        self.builder.connect_signals(self)

        self.tree = self.builder.get_object("package-list")
        self.package_detail = self.builder.get_object("package-detail")

        win = self.builder.get_object("main-window")
        win.set_application(self)
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

    def on_entry_activate(self, entry):
        packages = self.simple_query(entry.get_text())
        model = PackageList(packages)
        self.tree.set_model(model)

    def on_package_click(self, tree_view, path, column):
        model = tree_view.get_model()
        package = model.get_package(path)
        self.package_detail.set_package(package)
