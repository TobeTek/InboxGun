import json
from dataclasses import dataclass
from typing import Callable, Dict

from domain import common, triggers


@dataclass
class Action:
    step: common.Step
    workflow_id: str

    def run(self):
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


@dataclass
class SendMailAction(Action):
    def run(
        self,
        triggers_types: Dict,
        conditions_types: Dict,
        actions_types: Dict,
        add_subscriber: Callable,
    ):
        data = json.loads(self.step.step_data)
        target_emails = data["target_emails"]
        print(f"Sending Emails to {target_emails}")

        for step in self.step.children_steps:
            process = step.run(
                triggers_types=triggers_types,
                conditions_types=conditions_types,
                actions_types=actions_types,
            )

            if isinstance(process, triggers.Trigger):
                add_subscriber(process, process.trigger_event)

            elif isinstance(process, Action):
                process.run(
                    triggers_types=triggers_types,
                    conditions_types=conditions_types,
                    actions_types=actions_types,
                    add_subscriber=add_subscriber,
                )
