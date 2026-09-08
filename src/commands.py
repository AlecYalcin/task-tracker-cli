from receivers import TaskManager, TaskStatus

class Command:
    task_manager = TaskManager

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def execute(self, *args) -> None:
        raise NotImplementedError

class CreateTaskCommand(Command):
    def execute(self, description: str, *args):
        task_id = self.task_manager.create_task(description=description)
        print(f"Task added succesfully (ID: {task_id})")

class UpdateTaskCommand(Command):
    def execute(self, task_id: int, new_description: str | None = None, *args):
        self.task_manager.update_task(task_id, description=new_description)

class MarkInProgressCommand(Command):
    def execute(self, task_id: int, *args):
        self.task_manager.update_task(task_id, status=TaskStatus.IN_PROGRESS)

class MarkDoneCommand(Command):
    def execute(self, task_id: int, *args):
        self.task_manager.update_task(task_id, status=TaskStatus.DONE)

class DeleteTaskCommand(Command):
    def execute(self, task_id: int, *args):
        self.task_manager.delete_task(task_id)

class ListTasksCommand(Command):
    def execute(self, status: str | None = None, *args):
        try:
            status = TaskStatus(status)
        except ValueError:
            status = None
        tasks = self.task_manager.list_tasks(status=status)

        print("| ID \t| Description \t| Status \t| CreatedAt \t\t\t| UpdatedAt \t\t\t|")
        for task in tasks:
            task_status = f"{task.status}\t" if task.status == TaskStatus.IN_PROGRESS else f"{task.status}\t\t"
            print(f"| {task.id} \t| {task.description}\t| {task_status}| {task.createdAt}\t| {task.updatedAt}\t|")

