from datetime import datetime
from typing import Any, List, Optional
from dataclasses import dataclass, field
from .common import Step

from domain.utils import generate_random_id

@dataclass
class Workflow:
    
    status: str
    name: str
    step: Step = None
    id: str  = field(default_factory= generate_random_id) # UUID
    user_id: str  = field(default_factory=generate_random_id) # UUID to a User Model
    

    @classmethod
    def create_workflow(cls, user_id, name, status="completed", step: Step = None):
        """Create a new workflow"""
        workflow = cls(user_id=user_id, name=name, status=status, step=step)
        return workflow

    def add_trigger_step(self, step: Step, session):
        self.step = step
        session.add(self.step)
        session.commit()
        session.refresh(self)

    def add_children_steps(self, steps_data, session):
        if self.step is None:
            raise ValueError("Can not add children steps to null trigger step")
        
        parent_step = self.step
        for step in steps_data:
            Step.create_steps_from_json_tree(parent_id=parent_step.id, workflow_id=self.id, step_type=step["step_type"], children_steps = step["steps"], session=session)
        session.refresh(parent_step)
        return parent_step

    def run(self):
        self.step.process_step()

    @staticmethod
    def retrieve_workflow_from_db(id, session):
        return session.query(Workflow).filter(Workflow.id == id).first()

example_workflow = {
    "user": "user_109023",
    "workflow_id": "workflow_109203",
    "status": "Not published",  # Running, Stopped
    # Start Trigger is the Trigger type that initiates the running of the whole workflow.
    # An events microservice would filter all workflows that have start_trigger equal to an event and run them
    "start_trigger": {},
    # Steps in the the Workflow
    "steps": [
        {
            "type": "trigger:opt-in",
            "list": "Rich Dads Age 20-30",
            "steps": {"type": "action:"},
        }
    ],
}
