from domain.workflows import Workflow

{"trigger:opt-in": None}


def create_workflow(workflow_data: dict):
    workflow = Workflow(**workflow_data)
    workflow.persist()
