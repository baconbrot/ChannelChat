from importlib import import_module
from pkgutil import iter_modules

import channelchat


def init():
    package_infos = iter_modules(channelchat.events.handlers.__path__, prefix='channelchat.events.handlers.')
    for info in package_infos:
        if info.ispkg: continue
        import_module(info.name)