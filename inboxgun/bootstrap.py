"""Config for Project and EDA"""

import copy
from collections import defaultdict, deque
from typing import Callable, Deque, List

from .domain import actions, conditions, events, triggers  # noqa

TRIGGER_TYPES = {
    "trigger:opt-in": triggers.OptInTrigger,
    "trigger:time": triggers.TimeTrigger,
    "trigger:remove-from-list": triggers.RemoveFromListTrigger,
}

ACTION_TYPES = {
    "action:send-mail": actions.SendMailAction,
}

EVENT_HANDLERS = defaultdict(list)
EVENT_HANDLERS.update(
    {
        events.CustomerOptIn: [],
        events.CustomerRemoveFromList: [],
    }
)


def add_subscriber(subscriber, event_type):
    """Add a new subscriber for an event

    Args:
        subscriber (_type_): An object that has a `process_event` method
        event_type (_type_): An event data type
    """
    print(f"Adding subscriber {subscriber}, {event_type}")
    EVENT_HANDLERS[event_type].append(subscriber)


def remove_subscriber(subscriber, event_type):
    """Remove a subscriber from an event

    Args:
        subscriber (_type_): An object that has a `process_event` method
        event_type (_type_): An event data type
    """
    EVENT_HANDLERS[event_type].remove(subscriber)


def handle_event(event: events.Event, event_queue: Deque[events.Event] = None):
    """
    Called whenever a new event is received

    Args:
        event (events.Event): An instance of an event type
        event_queue (List[events.Event], optional): Serves as an accumulator for events that are raised. Defaults to None.
    """
    if event_queue is None:
        event_queue = deque()
    event_queue.appendleft(event)

    for event in event_queue:
        subscribers = EVENT_HANDLERS[type(event)].copy()
        for subscriber in subscribers:
            subscriber.process_event(
                event,
                event_queue,
                triggers_types=TRIGGER_TYPES,
                conditions_types=None,
                actions_types=ACTION_TYPES,
                add_subscriber=add_subscriber,
                remove_subscriber=remove_subscriber,
            )


def get_trigger_types():
    """Retrieve trigger types for the project"""
    return TRIGGER_TYPES


def get_action_types():
    """Retrieve trigger types for the project"""
    return ACTION_TYPES


def get_condition_types():
    """Retrieve trigger types for the project"""
    raise NotImplementedError
