from importlib import import_module
from pkgutil import walk_packages, iter_modules

from channelchat import events


def init():
    package_infos = iter_modules(events.handlers.__path__, prefix='events.handlers.')
    for info in package_infos:
        if info.ispkg: continue
        import_module(info.name)