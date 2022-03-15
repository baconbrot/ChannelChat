from channelchat.events.eventType import EventType

_listeners = {}


async def trigger(event_type: EventType, *args):
    if event_type == EventType.VOICE_STATE_UPDATE:
        try:
            for task in _listeners.get(event_type.value):
                await task(*args)
        except:
            print(f'[LOG] No task for event {event_type.name}')


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
