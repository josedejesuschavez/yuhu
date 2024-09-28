from abc import ABC, abstractmethod
from typing import List

from tasks.domain.task import Task


class TaskRepository(ABC):

    @abstractmethod
    def get_task_by_id(self, id: str) -> Task:
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        pass

    @abstractmethod
    def insert_task(self, task: Task):
        pass

    @abstractmethod
    def update_title_or_description_by_id(self, id: str, new_title: str, new_description: str):
        pass

    @abstractmethod
    def delete_task_by_id(self, id: str):
        pass