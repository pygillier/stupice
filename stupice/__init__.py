from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Notify  # noqa

APP_NAME = "stupice"
# Glade files folder, casted from PosixPath to str
GLADE_DIR = Path(__file__).parent / "views"

MEDIAS_ROOT = Path(__file__).parent / "medias"

# Init Notify connection
Notify.init(APP_NAME)
