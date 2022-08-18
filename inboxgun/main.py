from collections import defaultdict
from domain import triggers 
from domain import events
from domain.common import Step
from db.orm import session

import bootstrap


def test():
    q = session.query(Step).filter(Step.id == 2).first()
    # t = triggers.OptInTrigger(step=q, workflow_id=q.workflow_id)
    t = q.run(triggers=bootstrap.get_trigger_types(), conditions=None, actions=None)
    bootstrap.add_subscriber(t, events.CustomerOptIn)
    print(bootstrap.get_event_handlers())

    event = events.CustomerOptIn(customer_id="customer_2012", customer_list="Adults that went to Harvard", reason="I'm bored. Lemme alone")
    bootstrap.handle_event(event)

test()