from dataclasses import dataclass, field
from typing import Callable, Dict
from uuid import uuid4

from . import actions, common, events


@dataclass
class Trigger:
    """Trigger object"""

    trigger_event: events.Event
    trigger_id: str = field(default_factory=lambda: uuid4().hex)

    @staticmethod
    def process_event(self, event, event_queue):
        """Run the trigger"""
        raise NotImplementedError


@dataclass(kw_only=True)
class TimeTrigger(Trigger):
    """Execute children steps when a particular date/time is reached"""

    trigger_event: events.Event = (
        None  # Because it is time based, it does not subscribe to events
    )


@dataclass(kw_only=True)
class OptInTrigger(Trigger):
    """
    The opt-in element will be used to trigger actions in the automation sequence when someone
    opts-in to a list through a sign-up form created in InboxGun
    """

    workflow_id: str
    step: common.Step

    trigger_event: events.Event = events.CustomerOptIn

    def process_event(
        self,
        event,
        event_queue,
        triggers_types: Dict,
        conditions_types: Dict,
        actions_types: Dict,
        add_subscriber: Callable,
        remove_subscriber: Callable,
    ):
        remove_subscriber(self, self.trigger_event)

        print(f"Trigger: {self.trigger_id} Processing {type(event)}")

        for step in self.step.children_steps:
            process = step.run(
                triggers_types=triggers_types,
                conditions_types=conditions_types,
                actions_types=actions_types,
            )
            if isinstance(process, Trigger):
                add_subscriber(process, process.trigger_event)

            elif isinstance(process, actions.Action):
                process.run(
                    triggers_types=triggers_types,
                    conditions_types=conditions_types,
                    actions_types=actions_types,
                    add_subscriber=add_subscriber,
                )


@dataclass
class RemoveFromListTrigger(Trigger):
    trigger_event: events.Event = events.CustomerRemoveFromList
