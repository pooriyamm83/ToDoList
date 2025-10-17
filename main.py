from services.todo_manager import ToDoManager

def print_project_summary(p):
    print(f"[{p.id}] {p.name} - {p.description} (tasks: {len(p.tasks)})")

def print_task_summary(t):
    dl = t.deadline.isoformat() if t.deadline else None
    print(f"[{t.id}] {t.title} | {dl} | {t.status}")

def seed_demo(manager: ToDoManager):
    """create a demo project and tasks so user can see immediately"""
    try:
        p = manager.create_project("Demo Project", "A short demo")
        manager.add_task(p.id, "Buy milk", "One bottle", "todo", "2025-12-31")
        manager.add_task(p.id, "Write notes", "phase1 description", "doing")
    except Exception as e:
        print("Seed error:", e)

def main():
    manager = ToDoManager()
    seed_demo(manager)

    print("Simple To Do CLI. you can type help to see all commands.")
    while True:
        cmd = input(">>> ").strip()
        if cmd in ("exit", "quit"):
            print("Goodbye.")
            break

        # command handling
        if cmd == "help":
            print("commands: projects, create_project, delete_project, tasks <project_id>, ..., quit")
            continue

        if cmd == "projects":
            projects = manager.list_projects()
            if not projects:
                print("No projects found.")
            for p in projects:
                print_project_summary(p)
            continue

        if cmd.startswith("create_project"):
            # Usage: create_project ProjectName | optional description after |
            try:
                _, rest = cmd.split(" ", 1)
            except ValueError:
                print("Usage: create_project <name> | <description (optional)>")
                continue
            parts = rest.split("|", 1)
            name = parts[0]
            desc = parts[1].strip() if len(parts) > 1 else ""
            try:
                p = manager.create_project(name, desc)
                print("Created project:", p.id, p.name)
            except Exception as e:
                print("Error: ", e)
            continue

        if cmd.startswith("delete_project"):
            try:
                _, pid = cmd.split()
                pid = int(pid)
                ok = manager.delete_project(pid)
                print("Deleted project:", p.id if ok else "Project not found.")
            except Exception as e:
                print("Error: ", e)
            continue

        if cmd.startswith("tasks"):
            try:
                _, pid = cmd.split()
                pid = int(pid)
                tasks = manager.list_tasks(pid)
                if not tasks:
                    print("no tasks found int your desired project.")
                for t in tasks:
                    print_task_summary(t)
            except Exception as e:
                print("Error: ", e)
            continue

        # add_task <project_id> <title> | <description> | <status> | <deadline>
        if cmd.startswith("add_task"):
            try:
                _, rest = cmd.split(" ", 1)
                pid_str, rest = rest.split(" ", 1)
                pid = int(pid_str)
                parts = [p.strip() for p in rest.split("|", 1)]
                title = parts[0]
                desc1 = parts[1] if len(parts) > 1 else ""
                status = parts[2] if len(parts) > 2 else ""
                deadline = parts[3] if len(parts) > 3 else None
                t = manager.add_task(pid, title, desc1, status, deadline)
                print("Added task:", t.id, t.title)
            except Exception as e:
                print("Error:", e)
        continue

        print("Unknown command. type 'help'")
if __name__ == '__main__':
    main()