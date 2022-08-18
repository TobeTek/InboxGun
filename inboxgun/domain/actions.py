from inboxgun.domain.common import Step
import json

class Action:
    step: Step
    def run(self):
        pass
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

class SendMailAction(Action):
    def run(self):
        data = json.loads(self.step_data)
        target_emails = data["target_emails"]
        print(f"Sending Emails to {target_emails}")
        