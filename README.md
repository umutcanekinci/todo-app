# ToDo Application

This is a simple **To-Do List** application built with Python and Tkinter. It allows users to manage their tasks with features like adding tasks, setting statuses, and persisting data. The project is designed with a modular structure and incorporates various widgets for the UI.

---

![Screenshot 2025-01-13 144107](https://github.com/user-attachments/assets/a68b43d9-a9bb-4434-83b6-d857bf4755c1)
![Screenshot 2025-01-13 144146](https://github.com/user-attachments/assets/de13f5b0-9bc7-4c4e-87f8-181674ff6870)
![image](https://github.com/user-attachments/assets/d78b35ca-a02a-4534-9e4f-369247bf5f68)


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
  - All tasks are saved to a local database file (`database.db`) for persistence.  
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

. <br />
├── assets/ <br />
├── scripts/ <br />
│   ├── widgets/ <br />
│   │   ├── constants.py <br />
│   │   ├── database.py <br />
│   │   ├── enums.py <br />
│   │   ├── gui.py <br />
│   │   ├── main.py <br />
│   │   ├── rect.py <br />
│   │   └── utils.py <br />
├── .gitignore <br />
├── README.md <br />
├── requirements.txt <br />
└── todo.txt <br />

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
```bash
git clone https://github.com/umutcanekinci/todo-app.git
```

2. Create a virtual environment. (Optional)
    
      2.1 If pip is not in your system, install it first from [here](https://pip.pypa.io/en/stable/installation/)
      
      2.2 Then install virtualenv if you don't have.
      ```bash
      pip install virtualenv
      ```
      
      2.3 Go in directory
      ```bash
      cd todo-app
      ```

      2.3 Create virtual environment
      ```bash
      python -m venv .venv  
      ```
      
      2.4 Activate virtual environment
      ```bash
      .venv\Scripts\activate
      ```

2. Install required packages with pip
```bash
pip install -r requirements.txt  
```

4. Run the application
```bash
python scripts/main.py
```

Enjoy managing your tasks efficiently! 😊
