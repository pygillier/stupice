from loguru import logger
from . import GLADE_DIR, MEDIAS_ROOT
from .state import Countdown
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa


class App(Gtk.Application):
    def __init__(self):

        # Init styles
        # Init CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(str(MEDIAS_ROOT / "styles.css"))
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Init UI
        self.builder = Gtk.Builder()
        self.builder.add_from_file(str(GLADE_DIR / "main.glade"))
        self.builder.connect_signals(self)

        self.countdown = Countdown(
            builder=self.builder,
            counter=30
        )

        window = self.builder.get_object("main")
        window.show_all()

    @staticmethod
    def run():
        Gtk.main()

    @staticmethod
    def on_destroy(*args) -> None:
        """Stop application"""
        logger.info("Exiting...")
        Gtk.main_quit()

    def on_stop(self, button):
        logger.debug("Stopping counter")
        self.countdown.stop()

    def on_start(self, button):
        if self.countdown.is_stopped:
            self.countdown.start()
        elif self.countdown.is_started:
            self.countdown.pause()
        elif self.countdown.is_paused:
            self.countdown.restart()
