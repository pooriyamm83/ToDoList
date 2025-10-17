# ToDoList – Python OOP (In-Memory)📝

In this project i have developed a Command-Line Interface (CLI) project and task management application using Object-Oriented Programming (OOP) principles in Python.

*All data (tasks and projects) are currently stored In-Memory and will be lost upon program termination.*

This project was developed as part of Phase 1 of the Software Engineering course at Amirkabir University of Technology (AUT).

## Key Features🚀

| Capability | Description |
| :---: | :--- |
| Project Management | Create, edit, and delete projects. Deleting a project automatically removes all its associated tasks (Cascade Delete). |
| Task Management | Add, edit, and delete tasks within any project. |
| Task Status | Tasks can be updated to one of three statuses: todo, doing, or done. |
| Viewing Data | View the list of all projects and the tasks associated with each project. |


# Tech Stack & Prerequisites🛠️
Language: Python 3.11 or higher.

Dependencies: Managed via pip.

Configuration: Uses the python-dotenv library to read application limits from the .env file.


# Installation and Usage💡
Follow these steps to set up and run the application.

1. Create a Virtual Environment:

  I personally used a virtual environment and recommend to use virtual environment to isolate project dependencies:

```bash
python -m venv venv
```
# Activate on Windows:
```
.\venv\Scripts\activate
```
# Activate on Linux/macOS:
```
source venv/bin/activate
```

2. Install Dependencies:

  Install all required libraries using pip. You need to either have a requirements.txt file or install the dependencies manually (at minimum, python-dotenv is required):

```Bash

# Assuming you have a requirements.txt file:
pip install -r requirements.txt

# OR, install required library manually:
# pip install python-dotenv
```

3. Set Up Configuration:

  This part is very important make sure to create a file named .env in the project root to define application limits:


# .env file content
```
MAX_NUMBER_OF_PROJECT=10
MAX_NUMBER_OF_TASK=50
```
4. Run the Application:

  Execute the main file to start the CLI:

```Bash
python main.py
```

5. CLI Commands:

  Upon execution, a demo project is automatically created. To view the list of available commands, type help:

>>> help


## Project Structure
| File/Folder | Purpose |
| :---: | :--- |
| main.py | The main entry point and Command-Line Interface (CLI) implementation. |
| services/todo_manager.py | Service Layer: Contains the core business logic, including project and task management, validation, and in-memory data handling. |
| services/init.py | Marks the services directory as a Python package. |
| models/project.py | Data Model: Defines the Project class, which represents a project containing multiple Task objects. |
| models/task.py | Data Model: Defines the Task class, which represents an individual task with title, description, status, and deadline. |
| models/init.py | Marks the models directory as a Python package. |
| .env | Environment variables for configuration (e.g., MAX_NUMBER_OF_PROJECT, MAX_NUMBER_OF_TASK). Not committed to GitHub. |
| .gitignore | Specifies files and directories to be ignored by Git (e.g., .env, .venv, __pycache__/). |
