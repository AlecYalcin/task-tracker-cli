# task-tracker-cli

Task Tracker is a simple command line interface (CLI) to track what you need to do, what have you done and what you're currently working on. His purpose is to be a personal project to test programming skills and software engineering process at small applications.

## How to Run

Made with Python, you do not need any virtual environment to run this project. The only file that needs to be executed is `src/main.py` (Execute it in the base directory). The default utilization of this application is:

```txt
./src/main.py <command> <parameters>
- command: 'add', 'update', 'delete', 'mark-in-progress', 'mark-done', 'list'
- parameters: each command has it's own paramters.
```

### Create Tasks

```txt
./src/main.py add <description>
- description: task name or description
```

### Update Tasks

```txt
./src/main.py update <task-id> <new-description>
- task-id: integer that references the task you want to change
- new-description: task new name or description
```

### Delete Tasks

```txt
./src/main.py delete <task-id>
- task-id: integer that references the task you want to delete
```

### Change Tasks Status

```txt
./src/main.py mark-in-progress <task-id>
- task-id: integer that references the task you want to change it's status to 'In Progress'
```

```txt
./src/main.py mark-done <task-id>
- task-id: integer that references the task you want to change it's status to 'Done'
```

### List Tasks

```txt
./src/main.py list [<status>]
- status(opt.): 'todo', 'in-progress' or 'done', filters the results 
```

## Documentation

- [Project Chart](docs/project-chart.md)
- [Software Requirements Specification](docs/software-requirements.md)
- [User Stories](docs/user-stories.md)
- [Software Architechture Document](docs/architechture.md)
- [Data Model](docs/data-model.md)
