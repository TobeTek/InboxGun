"""Config for Project and EDA"""

from collections import defaultdict
from domain import triggers 
from domain import events
from typing import Callable, List


TRIGGER_TYPES = {
    "trigger:opt-in": triggers.OptInTrigger,
    "trigger:time": triggers.TimeTrigger,
    "trigger:remove-from-list": triggers.RemoveFromListTrigger,
}

EVENT_HANDLERS = defaultdict(list)
EVENT_HANDLERS.update({
    events.CustomerOptIn: [],
    events.CustomerRemoveFromList: [],
})

def handle_event(event: events.Event, event_queue: List[events.Event] = None):
    """
    Called whenever a new event is received

    Args:
        event (events.Event): An instance of an event type
        event_queue (List[events.Event], optional): Serves as an accumulator for events that are raised while processing. Defaults to None.
    """
    if event_queue is None:
        event_queue = list()
    for event in event_queue:
        for subscriber in EVENT_HANDLERS[type(event)]:
            subscriber(event, event_queue, triggers=TRIGGER_TYPES, conditions=None, actions=None)

def add_subscriber(subscriber: Callable, event_type: str):
    EVENT_HANDLERS[event_type].append(subscriber)

def add_triggers(trigger, event_type):
    TRIGGER_TYPES[event_type].append(trigger)

def get_trigger_types():
    return TRIGGER_TYPES

def get_event_handlers():
    return EVENT_HANDLERS
