from importlib import import_module
from pkgutil import walk_packages

from channelchat import events


def init():
    for info in walk_packages(events.handlers.__path__, prefix='events.handlers.'):
        if info.ispkg: continue
        import_module(info.name)