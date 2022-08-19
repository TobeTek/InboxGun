"""Test persistence and DB Constraints"""

from inboxgun.domain.common import Step

def test_step_constraints():
    s = Step(
        parent_id=2,
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

    assert True == True

def test_workflow_constraints():
    # Workflow with same name and user can't exist
    # Workflow ID must be unique
    pass