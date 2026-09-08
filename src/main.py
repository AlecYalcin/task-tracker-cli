import sys
from receivers import TaskManager, TaskRepository
from commands import (
    Command,
    CreateTaskCommand,
    UpdateTaskCommand,
    DeleteTaskCommand,
    MarkInProgressCommand,
    MarkDoneCommand,
    ListTasksCommand
)


class Interface:
    filename: str
    task_manager: TaskManager
    commands: dict[str, Command]

    def __init__(self, filename: str = "database.json"):
        repository = TaskRepository(filename=filename)
        self.task_manager = TaskManager(repository)
        self._initialize_commands()

    def _initialize_commands(self):
        self.commands = {}
        self.commands["add"] = CreateTaskCommand(task_manager=self.task_manager)
        self.commands["update"] = UpdateTaskCommand(task_manager=self.task_manager)
        self.commands["delete"] = DeleteTaskCommand(task_manager=self.task_manager)
        self.commands["mark-in-progress"] = MarkInProgressCommand(task_manager=self.task_manager)
        self.commands["mark-done"] = MarkDoneCommand(task_manager=self.task_manager)
        self.commands["list"] = ListTasksCommand(task_manager=self.task_manager)

    def execute_command(self, command: str, parameters: list[str]):
        registered_command = self.commands.get(command)
        if registered_command is None:
            print("Command not found")
            return
        registered_command.execute(*parameters)

if __name__ == "__main__":
    interface = Interface()
    command = sys.argv[1]
    parameters = sys.argv[2:]
    interface.execute_command(command, parameters)