import xbmc, os, threading
from kodipopcorntime.common import plugin, PLATFORM, CACHE_DIR
from contextlib import contextmanager, closing

LOCKS = {}

@contextmanager
def shelf(filename, ttl=0):
    import shelve
    filename = os.path.join(CACHE_DIR, filename)
    with LOCKS.get(filename, threading.RLock()):
        with closing(shelve.open(filename, writeback=True)) as d:
            import time
            if not d:
                d.update({
                    "created_at": time.time(),
                    "data": {},
                })
            elif ttl > 0 and (time.time() - d["created_at"]) > ttl:
                d["data"] = {}
