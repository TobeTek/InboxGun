from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4
from . import events
from .common import Step
from typing import Dict

@dataclass
class Trigger:
    """Trigger object"""
    trigger_event: events.Event
    trigger_id: str = field(default_factory=lambda: uuid4().hex)
    
    @staticmethod
    def process_event(self, event, event_queue):
        """Run the trigger"""
        raise NotImplementedError
    
    def __call__(self, event, event_queue):
        return self.process_event(event, event_queue)

@dataclass
class TimeTrigger(Trigger):
    """Execute children steps when a particular date/time is reached"""

    trigger_event: events.Event = None # Because it is time based, it does not subscribe to events

    def process_event(self, event, event_queue):
        print(f"Processing {event=}")
        for step in self.step.children_steps:
            step.run()

@dataclass(kw_only=True)
class OptInTrigger(Trigger):
    """
    The opt-in element will be used to trigger actions in the automation sequence when someone
    opts-in to a list through a sign-up form created in InboxGun
    """
    workflow_id: str
    step: Step

    trigger_event: events.Event = events.CustomerOptIn

    def process_event(self, event, event_queue, triggers: Dict, conditions: Dict, actions: Dict):
        print(f"Processing {event=}")
        for step in self.step.children_steps:
            step.run(triggers, conditions, actions)

@dataclass
class RemoveFromListTrigger(Trigger):
    pass

@dataclass
class TimeTrigger:
    trigger_time: str  # Date in ISO Format datetime

    def schedule(self):
        """Add to scheduler"""
        raise NotImplementedError
