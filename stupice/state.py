from datetime import timedelta
from statemachine import StateMachine, State
from loguru import logger
from gi.repository import GLib, Notify


class Countdown(StateMachine):

    counter = 0

    timeout_id = None

    stopped = State('Stopped', initial=True)
    started = State('Started')
    paused = State('Paused')

    start = stopped.to(started)
    stop = started.to(stopped) | paused.to(stopped)
    pause = started.to(paused)
    restart = paused.to(started)

    tick = started.to(started)

    def __init__(self, builder, counter, *args, **kwargs):
        super(Countdown, self).__init__()

        # Store initial value
        self.initial = counter

        self.counter = counter
        self.builder = builder

        self.update_countdown()

    def on_start(self):
        logger.info("Starting")
        Notify.Notification.new(
            "Stupice",
            "Starting counter for {} minutes".format(self.human_readable_secs())
        ).show()
        self.update_countdown()
        self.timeout_id = GLib.timeout_add(1000, self.tick, None)
        self.toggle_buttons(is_running=True)

    def on_stop(self):
        logger.info("Stopping")
        self.toggle_buttons(is_running=False)
        self.clear_timer()

        # Reset to initial value
        self.counter = self.initial
        self.update_countdown()

    def on_pause(self):
        logger.debug('on_pause')
        self.toggle_buttons(is_running=False)
        self.clear_timer()

    def on_restart(self):
        logger.debug('on_restart')
        self.toggle_buttons(is_running=True)
        self.timeout_id = GLib.timeout_add(1000, self.tick, None)

    def on_tick(self, *args):
        # Decrement counter
        self.counter -= 1
        self.update_countdown()

        # Counter at end, stop everything
        if self.counter <= 0:
            self.stop()

        return True  # Mandatory for timeout_add

    def toggle_buttons(self, is_running):
        label = "gtk-media-pause" if is_running else "gtk-media-play"
        self.builder.get_object("btn_start").set_label(label)
        self.builder.get_object("btn_stop").set_sensitive(is_running)

    def human_readable_secs(self):
        d = timedelta(seconds=self.counter)
        minutes = (d.seconds // 60) % 60
        sec = d.seconds - minutes * 60

        return "{:0>2d}:{:0>2d}".format(
            minutes,
            sec)

    def update_countdown(self):
        self.builder.get_object("counter").set_text(self.human_readable_secs())

    def clear_timer(self):
        """Remove function from GLib loop and clear reference"""
        if self.timeout_id is not None:
            GLib.source_remove(self.timeout_id)
        self.timeout_id = None
