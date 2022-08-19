# InboxGun
An Automation Workflow Module written in Python

> Tested on `Python 3.10.1`


## Getting Started:
Install requirements
```bash
> pip install -r requirements.txt
```

To run a demo:
```bash
> python -m inboxgun.main
```

To run tests:

```bash
> pytest 
```

## TODO: 
 - Resume Workflow inbetween execution
 - Add support for timed triggers. They don't need to subscribe to events and can be handled by a scheduler.
 - Make the logic for Running next steps more 'DRY'.
