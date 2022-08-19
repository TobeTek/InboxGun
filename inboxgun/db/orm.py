import sqlalchemy as db
from sqlalchemy.orm import backref, mapper, relationship, sessionmaker

from inboxgun.domain.common import Step
from inboxgun.domain.workflows import Workflow

metadata = db.MetaData()
step_table = db.Table(
    "step",
    metadata,
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("step_type", db.String(255)),
    db.Column("workflow_id", db.String(255)),
    db.Column("is_starting_step", db.Boolean, server_default="false"),
    db.Column("step_data", db.String(255)),
    db.Column("parent_id", db.Integer, db.ForeignKey("step.id"), nullable=True),
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


workflow_table = db.Table(
    "workflow",
    metadata,
    db.Column("id", db.String(255), primary_key=True),
    db.Column("name", db.String(255)),
    db.Column("status", db.String(255)),
    db.Column("user_id", db.String(255)),
    db.UniqueConstraint(
        "name", "user_id", name="unique_name_for_user"
    ),  # User can not have two workflows with the same name
)
workflow_mapper = mapper(Workflow, workflow_table)

def get_session(engine):
    metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        return session
    finally:
        session.close()
