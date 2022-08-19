"""
Example Entrypoint

Similar to what you'd have at an API Endpoint
"""
from collections import deque
import bootstrap
from db.orm import get_session
from .domain import actions, conditions, events, triggers
from .domain.common import Step
from .domain.workflows import Workflow
import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///./here.sqlite3")
session = get_session(engine)

def sample_create_step():
    """Create a step and running it's downstream steps"""
    q = session.query(Step).filter(Step.id == 1).first()
    process = q.run(
        triggers_types=bootstrap.get_trigger_types(),
        conditions_types=None,
        actions_types=None,
    )
    print(process)
    if isinstance(process, triggers.Trigger):
        print("Adding subscriber")
        bootstrap.add_subscriber(process, process.trigger_event)

    elif isinstance(process, actions.Action):
        process.run(
            triggers=bootstrap.get_trigger_types(), conditions=None, actions=None
        )

    event = events.CustomerOptIn(
        customer_id="customer_2012",
        customer_list="Adults that went to Harvard",
        reason="I'm bored. Lemme alone",
    )
    for _ in range(10):
        bootstrap.handle_event(event)


def sample_create_and_run_workflow():
    """
    Create a workflow and run all connected steps

    Abstract the idea of running individual steps
    """
    w = Workflow(
        status="completed", name="Send Reminder Emails to Favourite subscribers"
    )
    q = session.query(Step).filter(Step.id == 1).first()
    w.persist_workflow(session)
    w.set_starting_step(q, session)
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
        reason="I'm bored. Lemme alone",
    )
    bootstrap.handle_event(event, event_queue=deque([]))


sample_create_and_run_workflow()
