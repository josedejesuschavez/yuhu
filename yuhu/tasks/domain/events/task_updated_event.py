class TaskUpdatedEvent:

    def __init__(self, task_id, title: str, email: str, description: str):
        self.task_id = task_id
        self.title = title
        self.email = email
        self.description = description

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'email': self.email,
            'description': self.description,
        }