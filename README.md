# ToDo Application

This is a simple **To-Do List** application built with Python and Tkinter. It allows users to manage their tasks with features like adding tasks, setting statuses, and persisting data. The project is designed with a modular structure and incorporates various widgets for the UI.

---

## Features

### Implemented Features:
- **Task Management**:  
  Users can add tasks to a list with a title and optional description.
- **Status Management**:  
  Each task has three statuses:  
  - Open  
  - In Progress  
  - Done  
  Open tasks cannot be directly moved to "In Progress".
- **Data Persistence**:  
  - All tasks are saved to a local JSON file (`database.db`) for persistence.  
  - Upon reopening the app, tasks are restored.
- **Themes**:  
  A dark and light mode can be toggled (currently in progress).
- **Due Date**:  
  Tasks can be assigned a due date. Overdue tasks will eventually be highlighted in red (not yet implemented).

---

## Bugs & Known Issues

### Fixed Bugs:
- **Minimize Button**:  
  The minimize button was initially too small but has been fixed.
- **Exit Button**:  
  The exit button's appearance has been corrected.
- **Logo and Info Button**:  
  Adjusted to appear white as per the theme.
- **Last Element Deletion Freeze**:  
  Deleting the last task caused a freeze, which is now resolved.
- **Unlimited Tasks**:  
  Added a limit to prevent infinite tasks from being added.

### Open Issues:
- **Scrollbar**:  
  There is no scrollbar for the task list, causing usability issues with many tasks.
- **Alt+Tab Icon**:  
  The app icon does not appear in the taskbar when Alt+Tab is used.  
  [Related Question on StackOverflow](https://stackoverflow.com/questions/60442386/check-if-window-is-in-background-tkinter)
- **TopLevel Window Behavior**:  
  Sometimes, `TopLevel` windows (for details or editing) do not open correctly.
- **Status Filter**:  
  The ability to filter tasks by status (e.g., only show "Done" tasks) is not implemented yet.
- **Overdue Marking**:  
  Highlighting overdue tasks in red is a planned feature.

---

## Project Structure

The project is organized as follows:

ToDoApp/ ├── .vscode/ ├── assets/ # Stores application assets (e.g., images) ├── widgets/ # Contains custom widgets like buttons and tasks │ ├── button.py # Custom button widget │ ├── canvas.py # Used for rendering the canvas UI │ ├── task.py # Task management logic ├── .gitignore # Git ignore file ├── constants.py # Constants and global variables ├── database.db # SQLite database for task persistence ├── database.py # Handles database interactions ├── enums.py # Enums for task statuses ├── gui.py # Main GUI logic ├── gui2.py # Secondary GUI module ├── main.py # Application entry point ├── rect.py # Handles rectangle rendering ├── todo.txt # Temporary notes or storage ├── utils.py # Helper utilities


---

## Canvas Usage

The app uses a **Canvas** widget for rendering complex layouts.  
[Why Use Canvas Over Labels?](https://stackoverflow.com/questions/78168757/when-should-i-use-a-canvas-vs-a-label#:~:text=If%20you%20need%20to%20display,a%20frame%20aren't%20scrollable)

---

## Future Enhancements
- **Task Filtering**:  
  Filter tasks based on their statuses.
- **Search**:  
  Search for tasks by title.
- **Theme Support**:  
  Full implementation of light and dark themes.
- **Professional/Personal Tasks**:  
  Separate views for personal and professional tasks.
- **Overdue Marking**:  
  Highlight overdue tasks in red.

---

## How to Run

1. Clone the repository.
2. Install Python 3.10+ and required packages:
   ```bash
   pip install -r requirements.txt

3. Run the application

python main.py

Enjoy managing your tasks efficiently! 😊