import sys
from typing import List, Optional
from app.db.session import get_session
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.task import Status as TaskStatus
from app.commands.autoclose_overdue import autoclose_overdue
from app.exceptions.repository_exceptions import NotFoundError, DuplicateError, LimitExceededError
from app.exceptions.service_exceptions import ValidationError
from datetime import datetime


class ConsoleCLI:
    """Command-line interface for managing the ToDoList. Uses the Service layer."""

    def __init__(self):
        # Since the CLI runs for a long time, we do NOT open a session in __init__.
        # A new session is opened and closed for each command (in _execute_command).
        pass

    def _execute_command(self, handler, args):
        """
        Wrapper for managing the session lifecycle (open, execute, close).
        This prevents leaving sessions open indefinitely.
        """
        db_gen = get_session()
        db = next(db_gen)

        try:
            # Create services using a new Session
            project_service = ProjectService(db)
            task_service = TaskService(db)

            # Execute the command
            handler(args, project_service, task_service)

        except (NotFoundError, DuplicateError, LimitExceededError, ValidationError, ValueError) as e:
            # Catching defined application exceptions + validation errors
            print(f"❌ Error: {e}")
        except Exception as e:
            # Any unknown errors
            print(f"❌ Unknown error: {e}")
        finally:
            db.close()  # Always close the session

    # ----------------------------------
    # --- Project Handlers ---
    # ----------------------------------

    def _handle_project_create(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 1:
            raise ValueError("Project name is required: project-create <name> [description]")

        name = args[0]
        description = " ".join(args[1:]) if len(args) > 1 else ""

        project = project_service.create_project(name, description)
        print(f"✅ Project created with ID {project.id} and name '{project.name}'.")

    def _handle_project_list(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        projects = project_service.list_projects()
        if not projects:
            print("📣 No projects found.")
            return

        print("\n--- Project List ---")
        for p in projects:
            print(f"ID: {p.id} | Name: {p.name} | Description: {p.description}")
        print("---------------------\n")

    def _handle_project_edit(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 2:
            raise ValueError(
                "Project ID and fields are required: project-edit <id> [name=new_name] [description=new_desc]")

        project_id = int(args[0])
        updates = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                updates[key.lower()] = value

        if not updates:
            raise ValueError("No update fields provided.")

        updated_project = project_service.update_project(
            project_id,
            name=updates.get('name'),
            description=updates.get('description')
        )
        print(f"✅ Project {project_id} updated. New name: {updated_project.name}")

    def _handle_project_delete(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 1:
            raise ValueError("Project ID is required: project-delete <id>")

        project_id = int(args[0])
        project_service.delete_project(project_id)
        print(f"✅ Project {project_id} deleted successfully.")

    # ----------------------------------
    # --- Task Handlers ---
    # ----------------------------------

    def _handle_task_add(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 2:
            raise ValueError(
                "Project ID and task title are required: task-add <project_id> <title> [description] [due_date=YYYY-MM-DD]")

        project_id = int(args[0])
        title = args[1]
        description = ""
        due_date = None

        remaining_args = args[2:]
        if remaining_args:
            for arg in remaining_args:
                if arg.lower().startswith('due_date='):
                    due_date = arg.split('=', 1)[1]
                else:
                    description = arg

        task = task_service.create_task(project_id, title, description, due_date=due_date)
        print(f"✅ Task '{task.title}' (ID {task.id}) added to project {project_id}.")

    def _handle_task_list(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 1:
            raise ValueError("Project ID is required: task-list <project_id>")

        project_id = int(args[0])

        project = project_service.get_project(project_id)
        tasks = task_service.list_tasks(project_id)

        print(f"\n--- Tasks for Project: {project.name} (ID: {project.id}) ---")
        if not tasks:
            print("📣 No tasks found in this project.")
            return

        for t in tasks:
            status_emoji = '✅' if t.status == TaskStatus.DONE else ('⏳' if t.status == TaskStatus.TODO else '🛠️')
            due = f" | Due: {t.due_date}" if t.due_date else ""
            print(f"ID: {t.id} | Status: {t.status.value.upper()} {status_emoji} | Title: {t.title}{due}")
        print("--------------------------------------------------\n")

    def _handle_task_status(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 2:
            raise ValueError("Task ID and new status are required: task-status <id> <todo|doing|done>")

        task_id = int(args[0])
        new_status_str = args[1].lower()

        if new_status_str not in [s.value for s in TaskStatus]:
            raise ValueError(f"Invalid status. Allowed: {[s.value for s in TaskStatus]}")

        task_service.update_task_status(task_id, TaskStatus(new_status_str))
        print(f"✅ Task {task_id} status changed to '{new_status_str.upper()}'.")

    def _handle_task_edit(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 2:
            raise ValueError(
                "Task ID and fields are required: task-edit <id> [title=...] [description=...] [due_date=YYYY-MM-DD]")

        task_id = int(args[0])
        updates = {}
        for arg in args[1:]:
            if '=' in arg:
                key, value = arg.split('=', 1)
                updates[key.lower()] = value

        if not updates:
            raise ValueError("No update fields provided.")

        task_service.update_task(
            task_id,
            title=updates.get('title'),
            description=updates.get('description'),
            due_date=updates.get('due_date')
        )
        print(f"✅ Task {task_id} updated.")

    def _handle_task_delete(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        if len(args) < 1:
            raise ValueError("Task ID is required: task-delete <id>")

        task_id = int(args[0])
        task_service.delete_task(task_id)
        print(f"✅ Task {task_id} deleted successfully.")

    # ----------------------------------
    # --- System Handlers ---
    # ----------------------------------

    def _handle_overdue(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        """Executes the command that auto-closes overdue tasks."""
        autoclose_overdue()  # Manages its own session + commit
        print("✅ Overdue auto-close command executed.")

    def _show_help(self, args: List[str], project_service: ProjectService, task_service: TaskService):
        """Display help menu"""
        print("\n--- CLI Help ---")
        print("Project Commands:")
        print("  project-create <name> [description] - Create a new project")
        print("  project-list - List all projects")
        print("  project-edit <id> [name=new_name] [description=new_desc] - Edit a project")
        print("  project-delete <id> - Delete a project and all its tasks")
        print("\nTask Commands:")
        print("  task-add <project_id> <title> [description] [due_date=YYYY-MM-DD] - Add a task")
        print("  task-list <project_id> - List tasks of a project")
        print("  task-edit <id> [title=...] [description=...] [due_date=...] - Edit a task")
        print("  task-status <id> <todo|doing|done> - Change task status")
        print("  task-delete <id> - Delete a task")
        print("\nSystem Commands:")
        print("  overdue - Manually run overdue auto-close command")
        print("  help - Show this help menu")
        print("  exit - Exit the program")
        print("---------------------\n")

    def run(self):
        """Main CLI loop"""
        print("ToDoList CLI - Phase 2 (Layered Architecture) | Type 'help' for commands.")

        command_map = {
            "project-create": self._handle_project_create,
            "project-list": self._handle_project_list,
            "project-edit": self._handle_project_edit,
            "project-delete": self._handle_project_delete,
            "task-add": self._handle_task_add,
            "task-list": self._handle_task_list,
            "task-status": self._handle_task_status,
            "task-edit": self._handle_task_edit,
            "task-delete": self._handle_task_delete,
            "overdue": self._handle_overdue,
            "help": self._show_help,
            "exit": lambda args, ps, ts: sys.exit(0)
        }

        while True:
            cmd = input("> ").strip().split()
            if not cmd:
                continue

            action = cmd[0].lower()
            args = cmd[1:]

            handler = command_map.get(action)

            if handler:
                self._execute_command(handler, args)
            else:
                print(f"❌ Unknown command '{action}'. Try 'help'.")


if __name__ == "__main__":
    cli = ConsoleCLI()
    cli.run()
