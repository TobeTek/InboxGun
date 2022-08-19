from inboxgun.domain.common import Step


def test_create_step():
    s = Step(
        parent_id=2,
        children_steps=[],
        step_type="trigger:opt-in",
        step_data='{"trigger":"2019-20-01.10-23-12.1243"}',
        workflow_id="1",
    )

    # s.persist_step(session)
    # s2 = Step(
    #     parent_id=1,
    #     children_steps=[],
    #     step_type="action:send-mail",
    #     step_data='{"date":"2019-20-01.10-23-12.1243", "target_emails":["user1@email.com", "user2@email.com", "user3@email.com"]}',
    #     workflow_id="1",
    # )
    # s2.persist_step(session)
    # print(s,s2)
    # q = session.query(Step).filter(Step.id == 1).first()
    # print(q.children_steps)
    
    # Ensure step id is created

    # Ensure step children_steps is set


def test_create_steps_from_json():
    pass

# s = Step.create_from_json(**{
#     "workflow_id":"HelloWorld",
#     "step_type":"trigger:opt-in",
#     "parent_id": None,

#     "children_steps": [
#         {

#             "parent_id": "0",
#             "workflow_id":"HelloWorld",
#             "step_type":"action:send-mail",
#             "steps": []
#         },
#         {

#             "parent_id": "0",
#             "workflow_id":"HelloWorld",
#             "step_type":"action:send-mail",
#             "steps": [
#                 {

#                     "parent_id": "2",
#                     "workflow_id":"HelloWorld",
#                     "step_type":"trigger:schedule-action",
#                     "steps": []
#                 },
#                 {

#                    "parent_id": "2",
#                     "workflow_id":"HelloWorld",
#                     "step_type":"action:deactivate-user",
#                     "steps": []
#                 }
#             ]
#         },
#         {

#             "parent_id": "0",
#             "workflow_id":"HelloWorld",
#             "step_type":"action:send-mail",
#             "steps": [
#                 {

#                     "parent_id": "5",
#                     "workflow_id":"HelloWorld",
#                     "step_type":"trigger:schedule-action",
#                     "steps": []
#                 },
#                 {

#                    "parent_id": "5",
#                     "workflow_id":"HelloWorld",
#                     "step_type":"action:deactivate-user",
#                     "steps": []
#                 }
#             ]
#         }
#     ]

# })
# s.persist_step(session=session)
