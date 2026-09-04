from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import json

class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus
    createdAt: datetime
    updatedAt: datetime

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat()
        }

    @classmethod
    def from_json(cls, json_task: dict) -> "Task":
        return cls(
            id=json_task["id"],
            description=json_task["description"],
            status=TaskStatus(json_task["status"]),
            createdAt=datetime.fromisoformat(json_task["createdAt"]),
            updatedAt=datetime.fromisoformat(json_task["updatedAt"]),
        )

    def __eq__(self, other_task: any) -> bool:
        if isinstance(other_task, Task) and self.id == other_task.id:
            return True 
        return False

class TaskRepository:
    filename: str

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._create_file_if_not_exists()

    def _create_file_if_not_exists(self) -> None:
        import os
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                json.dump({}, f)

    def save(self, task: Task) -> None:
        data = self.retrieve()
        with open(self.filename, "w") as f:
            data[task.id] = task.to_json()
            json.dump(data, f)

    def delete(self, id: int) -> None:
        data = self.retrieve()
        with open(self.filename, "w") as f:
            data.pop(str(id))
            json.dump(data, f)

    def find(self, id: int) -> Task | None:
        with open(self.filename, "r") as f:
            data = json.load(f)
        task_json = data.get(str(id))
        if task_json:
            return Task.from_json(task_json)
        return task_json

    def retrieve(self, status: TaskStatus | None = None) -> list[Task]:
        with open(self.filename, "r") as f:
            data = json.load(f)
        if status:
            return {
                task_id: task
                for task_id, task in data.items()
                if task["status"] == status
            }
        return data

class TaskManager:
    repository: TaskRepository

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def _last_task_id(self) -> int:
        tasks = self.repository.retrieve()
        last_task: Task = tasks[len(tasks)-1]
        return last_task.id

    def create_task(self, description: str) -> None:
        self.repository.save(
            Task(
                id=self._last_task_id()+1,
                description=description,
                status=TaskStatus.TODO,
                createdAt=datetime.now(),
                updatedAt=datetime.now()
            )
        )

    def update_task(self, id: int, description: str | None, status: TaskStatus | None) -> None:
        task = self.repository.find(id)
        task.description = description or task.description
        task.status = status or task.status
        task.updatedAt = datetime.now()
        self.repository.save(task)

    def delete_task(self, id: int) -> None:
        self.repository.delete(id)

    def list_tasks(self, status: TaskStatus | None) -> None:
        tasks = self.repository.retrieve(status)
        print("ID \t | Description \t | Status \t | CreatedAt \t | UpdatedAt \t |")
        for task in tasks:
            print(f"{task.id} | {task.description} | {task.status} | {task.createdAt} | {task.updatedAt} |")

if __name__ == "__main__":
    filename = "task-cli-test.json"

    # Testes de Banco de Dados
    repository = TaskRepository(filename)

    ## Teste de Salvamento
    test_task = Task(id=1, description="tarefa-teste", status=TaskStatus.IN_PROGRESS, createdAt=datetime.now(), updatedAt=datetime.now())
    repository.save(test_task)
    found_task = repository.find(1)
    assert test_task == found_task
    found_task.status = TaskStatus.DONE
    repository.save(found_task)
    found_task = repository.find(1)
    assert found_task.status == TaskStatus.DONE
    repository.delete(1)
    found_task = repository.find(1)
    assert found_task == None

    # Testes de Unitários
    ...
