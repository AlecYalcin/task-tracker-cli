import os
from datetime import datetime
from receivers import TaskManager, TaskRepository, TaskStatus, Task

def test_repository(repository: TaskRepository):
    """ Tests create, update and delete from .json files with repository """

    # CREATE
    test_task = Task(id=1, description="tarefa-teste", status=TaskStatus.IN_PROGRESS, createdAt=datetime.now(), updatedAt=datetime.now())
    repository.save(test_task)
    found_task = repository.find(1)
    assert test_task == found_task

    # UPDATE
    found_task.status = TaskStatus.DONE
    repository.save(found_task)
    found_task = repository.find(1)
    assert found_task.status == TaskStatus.DONE

    # DELETE
    repository.delete(1)
    found_task = repository.find(1)
    assert found_task == None


def test_task_manager(repository: TaskRepository):
    """ Tests TaskManager functions: create, update, delete and list (with and without filters)"""
    task_manager = TaskManager(repository)

    # CREATE
    task_id = task_manager.create_task("tarefa-teste")
    task = repository.find(task_id)
    assert task.description == "tarefa-teste"
    assert task.status == TaskStatus.TODO

    # UPDATE
    task_manager.update_task(task_id, description="tarefa-teste-atualizada", status=TaskStatus.IN_PROGRESS)
    task_updated = repository.find(task_id)
    assert task_updated.description == "tarefa-teste-atualizada"
    assert task_updated.status == TaskStatus.IN_PROGRESS
    assert task_updated.updatedAt > task.updatedAt

    # DELETE
    task_manager.delete_task(task_id)
    task_deleted = repository.find(task_id)
    assert task_deleted is None

    # LIST
    task_id_1 = task_manager.create_task("tarefa-teste-1")
    task_id_2 = task_manager.create_task("tarefa-teste-2")
    task_id_3 = task_manager.create_task("tarefa-teste-3")
    task_id_4 = task_manager.create_task("tarefa-teste-4")

    tasks_found = task_manager.list_tasks()
    for task_found, equal_task in zip(tasks_found, [task_id_1, task_id_2, task_id_3, task_id_4]):
        assert task_found.id == equal_task

    # LIST with FILTER
    task_manager.update_task(task_id_1, status=TaskStatus.IN_PROGRESS)
    task_manager.update_task(task_id_3, status=TaskStatus.IN_PROGRESS)
    task_manager.update_task(task_id_4, status=TaskStatus.DONE)

    todo_tasks = task_manager.list_tasks(TaskStatus.TODO)
    inprogress_tasks = task_manager.list_tasks(TaskStatus.IN_PROGRESS)
    done_tasks = task_manager.list_tasks(TaskStatus.DONE)

    assert [task.id for task in todo_tasks] == [task_id_2]
    assert [task.id for task in inprogress_tasks] == [task_id_1, task_id_3]
    assert [task.id for task in done_tasks] == [task_id_4]

if __name__ == "__main__":
    filename = "task-cli-test.json"
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    repository = TaskRepository(filename)
    test_repository(repository=repository)
    test_task_manager(repository=repository)


