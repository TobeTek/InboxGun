import sqlalchemy
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import backref, mapper, relationship, sessionmaker

from domain.common import Step
from domain.workflows import Workflow

engine = sqlalchemy.create_engine("sqlite:///./here.sqlite3")
connection = engine.connect()

metadata = MetaData()
step_table = Table(
    "step",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("step_type", String(255)),
    Column("workflow_id", String(255)),
    Column("is_starting_step", Boolean, server_default="false"),
    Column("step_data", String(255)),
    Column("parent_id", Integer, ForeignKey("step.id"), nullable=True),
)
step_mapper = mapper(
    Step,
    step_table,
    properties={
        "parent": relationship(
            Step, backref="children_steps", remote_side=[step_table.c.id]
        ),
    },
)


workflow_table = Table(
    "workflow",
    metadata,
    Column("id", String(255), primary_key=True),
    Column("name", String(255)),
    Column("status", String(255)),
    Column("user_id", String(255)),
    UniqueConstraint(
        "name", "user_id", name="unique_name_for_user"
    ),  # User can not have two workflows with the same name
)
workflow_mapper = mapper(Workflow, workflow_table)

# lines_mapper = mapper(Step, step_table)
metadata.create_all(engine)

# from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

# s = Step(**{
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
