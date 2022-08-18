"""Common models and datatypes shared across the domain"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Step:
    """Generic Base class for steps in a Workflow"""    
    children_steps: List

    step_type: str
    step_data: str # JSON Data, could be a date in ISOFormat
    workflow_id: str
    
    parent_id: int = None
    id: int = field(init=False)

    def run(self, triggers: Dict = None, conditions: Dict = None, actions: Dict = None):
        # Check if trigger.
        # If yes, run
        # Trigger.schedule(data)
        if self.step_type.startswith("trigger:") and triggers is not None:
            print(triggers, self.step_type)
            trigger_cls = triggers[self.step_type]
            trigger = trigger_cls(workflow_id=self.workflow_id, step=self)
            return trigger

        # Check if action
        # If yes, run
        # Action.run(data)

        # Check if conditional
        # If yes, evaluate it
        # Check which branch to evaluate

    @classmethod
    def create_steps_from_json_tree(cls, parent_id, workflow_id, children_steps, step_type, session):
        parent_step = cls(parent_id=parent_id, workflow_id=workflow_id, step_type=step_type)
        parent_step.persist_step(session)

        for step in children_steps:
            Step.parse_steps_from_json_tree(parent_id=parent_step.id, workflow_id=workflow_id, step_type=step["step_type"], children_steps = step["steps"], session=session)

        session.refresh(parent_step)
        return parent_step

    def persist_step(self, session):
        session.add(self)
        session.commit()
        session.refresh(self)

    
    def __str__(self):
        return f"Step(id={self.id}, step_type={self.step_type}, step_data={self.step_data})"
    
    def __repr__(self) -> str:
        return self.__str__()