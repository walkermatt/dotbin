from importphotos import import_photos
from threading import Timer
import os
import pyinotify

src_dir = os.path.abspath(os.path.expanduser('~/Dropbox/Camera Uploads'))
dest_dir = os.path.abspath(os.path.expanduser('~/Dropbox/Photos/'))

def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                return fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

def watch_dir(src_dir, callback):
    wm = pyinotify.WatchManager()

    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_NOWRITE(self, event):
            callback(event)

    notifier = pyinotify.Notifier(wm, EventHandler())
    wm.add_watch(src_dir, pyinotify.IN_CLOSE_NOWRITE)
    notifier.loop()

@debounce(10)
def file_added(event):
    import_photos(False, src_dir, dest_dir)

# Watch the source directory for incoming
# files
watch_dir(src_dir, file_added)
