from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, List, Optional

from . import actions, common, triggers
from .utils import generate_random_id


@dataclass
class Workflow:
    """Adapter for Automation Steps"""
    status: str
    name: str
    id: str = field(default_factory=generate_random_id)  # UUID
    user_id: str = field(default_factory=generate_random_id)  # UUID to a User Model

    @classmethod
    def create_workflow(
        cls, user_id, name, status="completed", step: common.Step = None
    ):
        """Create a new workflow"""
        workflow = cls(user_id=user_id, name=name, status=status, step=step)
        return workflow

    def persist_workflow(self, session):
        """Save workflow to DB"""
        session.add(self)
        session.commit()
        session.refresh(self)

    def set_starting_step(self, step: common.Step, session):
        """Change/Set the first step for the workflow"""
        step.is_starting_step = True
        session.add(step)
        session.commit()
        session.refresh(self)

    def add_children_steps(self, steps_data, session):
        if self.step is None:
            raise ValueError("Can not add children steps to null trigger step")

        parent_step = self.step
        for step in steps_data:
            common.Step.create_steps_from_json_tree(
                parent_id=parent_step.id,
                workflow_id=self.id,
                step_type=step["step_type"],
                children_steps=step["steps"],
                session=session,
            )
        session.refresh(parent_step)
        return parent_step

    def run(
        self,
        add_subscriber: Callable,
        triggers_types,
        conditions_types,
        actions_types,
        session,
    ):
        starting_steps = (
            session.query(common.Step)
            .filter(common.Step.is_starting_step == True)
            .all()
        )
        print("Starting Workflow\nInitial Steps:", starting_steps)
        for step in starting_steps:
            process = step.run(
                triggers_types=triggers_types,
                conditions_types=conditions_types,
                actions_types=actions_types,
            )
            if isinstance(process, triggers.Trigger):
                add_subscriber(process, process.trigger_event)
            elif isinstance(process, actions.Action):
                process.run(
                    triggers=triggers,
                    conditions=None,
                    actions=None,
                    add_subscriber=add_subscriber,
                )

    @staticmethod
    def retrieve_workflow_from_db(id, session):
        return session.query(Workflow).filter(Workflow.id == id).first()
