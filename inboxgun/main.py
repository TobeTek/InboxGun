"""
Example Entrypoint

Similar to what you'd have at an API Endpoint
"""
from collections import deque

import sqlalchemy

from . import bootstrap
from .db.orm import get_session
from .domain import actions, conditions, events, triggers
from .domain.common import Step
from .domain.workflows import Workflow

engine = sqlalchemy.create_engine("sqlite:///./main.sqlite3")
session = get_session(engine)

def create_fixtures():
    Step(
        parent_id=None,
        children_steps=[],
        step_type="trigger:opt-in",
        step_data='{"trigger":"2019-20-01.10-23-12.1243"}',
        workflow_id="1",
    ).persist_step(session)

    s = Step(
        parent_id=1,
        children_steps=[],
        step_type="trigger:opt-in",
        step_data='{"trigger":"2019-20-01.10-23-12.1243"}',
        workflow_id="1",
    )
    s2 = Step(
        parent_id=1,
        children_steps=[],
        step_type="action:send-mail",
        step_data='{"date":"2019-20-01.10-23-12.1243", "target_emails":["user1@email.com", "user2@email.com", "user3@email.com"]}',
        workflow_id="1",
    )
    s.persist_step(session)
    s2.persist_step(session)

def sample_create_step():
    """Create a step and running it's downstream steps"""
    step = session.query(Step).filter(Step.id == 1).first()
    process = step.run(
        triggers_types=bootstrap.get_trigger_types(),
        conditions_types=None,
        actions_types=None,
    )
    if isinstance(process, triggers.Trigger):
        bootstrap.add_subscriber(process, process.trigger_event)

    elif isinstance(process, actions.Action):
        process.run(
            triggers=bootstrap.get_trigger_types(), conditions=None, actions=None
        )

    event = events.CustomerOptIn(
        customer_id="customer_2012",
        customer_list="Adults that went to Harvard",
        reason="Great Newsletter",
    )
    
    # Trigger all subscribers to that event
    bootstrap.handle_event(event)


def sample_create_and_run_workflow():
    """
    Create a workflow and run all connected steps

    Abstract the idea of running individual steps
    """
    w = Workflow(
        status="completed", name="Send Reminder Emails to Favourite subscribers"
    )
    s = Step(
        parent_id=None,
        children_steps=[],
        step_type="action:send-mail",
        step_data='{"date":"2019-20-01.10-23-12.1243", "target_emails":["user1@email.com", "user2@email.com", "user3@email.com"]}',
        workflow_id=w.id,
    )
    w.persist_workflow(session)
    w.set_starting_step(s, session)
    w.run(
        triggers_types=bootstrap.get_trigger_types(),
        conditions_types=None,
        actions_types=bootstrap.get_action_types(),
        session=session,
        add_subscriber=bootstrap.add_subscriber,
    )

    event = events.CustomerOptIn(
        customer_id="customer_2012",
        customer_list="Adults that went to Harvard",
        reason="Personal reasons",
    )
    bootstrap.handle_event(event, event_queue=deque([]))

create_fixtures()
sample_create_step()
sample_create_and_run_workflow()
