from collections import defaultdict
from domain import triggers 
from domain import events
from domain.common import Step
from db.orm import session

from typing import Callable, List


def test():
    q = session.query(Step).filter(Step.id == 2).first()
    # t = triggers.OptInTrigger(step=q, workflow_id=q.workflow_id)
    t = q.run(trigger_types=TRIGGER_TYPES, condition_types=None, action_types=None)
    add_subscriber(t, events.CustomerOptIn)
    print(EVENT_HANDLERS)

    event = events.CustomerOptIn(customer_id="customer_2012", customer_list="Adults that went to Harvard", reason="I'm bored. Lemme alone")
    handle_event(event)

test()