from channelchat.events import handlers
from channelchat.events.eventType import EventType


_listeners = {}


async def trigger(event_type: EventType, *args):
    if event_type == EventType.VOICE_STATE_UPDATE:
        for task in _listeners.get(event_type.value):
             await task(*args)


def register(event_type: EventType):
    def decorator(func):
        try:
            tasks = _listeners[event_type.value]
        except:
            tasks = []
        tasks.append(func)
        _listeners[event_type.value] = tasks
        return func
    return decorator


handlers.init()
