from typing import List
from .repository import ToDoListRepository
from .models.task import Task, Status


class ToDoListCLI:
    def __init__(self):
        self.repo = ToDoListRepository()
        self.commands = {
            "project-create": self.create_project,
            "project-list": self.list_projects,
            "project-edit": self.edit_project,
            "project-delete": self.delete_project,
            "task-add": self.add_task,
            "task-list": self.list_tasks,
            "task-status": self.change_task_status,
            "task-edit": self.edit_task,
            "task-delete": self.delete_task,
            "help": self.show_help,
            "exit": lambda _: exit(0)
        }

    def _find_project(self, partial_id: str):
        return self.repo.get_project(partial_id)

    def show_help(self, _):
        print("\nCommands:")
        print("  project-create <name> [description]     → Create a new project")
        print("  project-list                            → List all projects")
        print("  project-edit <id> <new-name> [desc]     → Edit project details")
        print("  project-delete <id>                     → Delete project (and its tasks)")
        print("  task-add <proj-id> <title> [desc] [due] → Add a new task")
        print("  task-list <proj-id>                     → List all tasks in a project")
        print("  task-status <proj-id> <task-id> <status> → Change task status")
        print("  task-edit <proj-id> <task-id> <title> [desc] [due] → Edit task details")
        print("  task-delete <proj-id> <task-id>         → Delete a task")
        print("  help                                    → Show this help message")
        print("  exit                                    → Exit the program\n")

    def create_project(self, args: List[str]):
        if len(args) < 1:
            print("Error: Project name is required.")
            return
        name = args[0]
        desc = " ".join(args[1:]) if len(args) > 1 else ""
        try:
            p = self.repo.create_project(name, desc)
            print(f"Project created: {p}")
        except Exception as e:
            print(f"Error: {e}")

    def list_projects(self, _):
        projects = self.repo.list_projects()
        if not projects:
            print("No projects found.")
            return
        print("\nProject List:")
        for p in projects:
            print(f"  {p} - {p.description[:50]}{'...' if len(p.description) > 50 else ''}")
        print()

    def edit_project(self, args: List[str]):
        if len(args) < 2:
            print("Error: project-edit <id> <new-name> [desc]")
            return
        proj = self._find_project(args[0])
        if not proj:
            print("Project not found.")
            return
        name = args[1]
        desc = " ".join(args[2:]) if len(args) > 2 else None
        if self.repo.update_project(proj.id, name, desc):
            print("Project updated successfully.")
        else:
            print("Error updating project.")

    def delete_project(self, args: List[str]):
        if not args:
            print("Error: project-delete <id>")
            return
        proj = self._find_project(args[0])
        if proj and self.repo.delete_project(proj.id):
            print("Project and all its tasks deleted (Cascade Delete).")
        else:
            print("Project not found.")

    def add_task(self, args: List[str]):
        if len(args) < 2:
            print("Error: task-add <proj-id> <title> [desc] [due]")
            return
        proj = self._find_project(args[0])
        if not proj:
            print("Project not found.")
            return
        title = args[1]
        desc = " ".join(args[2:-1]) if len(args) > 3 else ""
        due = args[-1] if len(args) > 2 and "-" in args[-1] else None
        try:
            task = Task(title, desc, "todo", due)
            proj.add_task(task)
            print(f"Task added: {task}")
        except Exception as e:
            print(f"Error: {e}")

    def list_tasks(self, args: List[str]):
        if not args:
            print("Error: task-list <proj-id>")
            return
        proj = self._find_project(args[0])
        if not proj or not proj.tasks:
            print("No tasks found.")
            return
        print(f"\nTasks in Project [{proj.id[:8]}]:")
        for t in proj.tasks:
            print(f"  {t}")
        print()

    def change_task_status(self, args: List[str]):
        if len(args) != 3:
            print("Error: task-status <proj-id> <task-id> <todo|doing|done>")
            return
        proj = self._find_project(args[0])
        if not proj:
            print("Project not found.")
            return
        task = proj.get_task_by_id(args[1])
        if not task:
            print("Task not found.")
            return
        try:
            task.update_status(args[2])
            print("Task status updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def edit_task(self, args: List[str]):
        if len(args) < 3:
            print("Error: task-edit <proj-id> <task-id> <title> [desc] [due]")
            return
        proj = self._find_project(args[0])
        if not proj:
            print("Project not found.")
            return
        task = proj.get_task_by_id(args[1])
        if not task:
            print("Task not found.")
            return
        title = args[2]
        desc = " ".join(args[3:-1]) if len(args) > 4 else task.description
        due = args[-1] if len(args) > 3 and "-" in args[-1] else task.due_date
        try:
            task.title = title
            task.description = desc
            task.due_date = due
            print("Task updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_task(self, args: List[str]):
        if len(args) != 2:
            print("Error: task-delete <proj-id> <task-id>")
            return
        proj = self._find_project(args[0])
        if proj and proj.remove_task(args[1]):
            print("Task deleted successfully.")
        else:
            print("Task not found.")

    def run(self):
        print("ToDoList CLI (Phase 1) - Type 'help' for a list of commands.")
        while True:
            try:
                inp = input("> ").strip()
                if not inp:
                    continue
                parts = inp.split()
                cmd, args = parts[0], parts[1:]
                handler = self.commands.get(cmd)
                if handler:
                    handler(args)
                else:
                    print("Invalid command. Try 'help'.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unknown error: {e}")
