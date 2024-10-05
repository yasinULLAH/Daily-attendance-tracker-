```markdown
# Student Attendance Tracker

A simple Python-based GUI application to manage and track student attendance. Built with Tkinter, this application allows educators to efficiently handle attendance records, ensuring accurate and organized tracking.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Manage Students](#manage-students)
  - [Mark Attendance](#mark-attendance)
  - [View Attendance](#view-attendance)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Data Persistence](#data-persistence)
- [Input Validation](#input-validation)
- [Extensibility](#extensibility)
- [License](#license)

## Features

- **Manage Students**: Add and view students with unique IDs.
- **Mark Attendance**: Mark students as present or absent for a selected date.
- **View Attendance**: View attendance records by date or by individual student.
- **Data Persistence**: Stores data in CSV files (`students.csv` and `attendance.csv`).
- **User-Friendly GUI**: Intuitive interface built with Tkinter.
- **Input Validation**: Ensures data integrity with checks for duplicate IDs and correct date formats.

## Installation

### Prerequisites

- **Python 3.x**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/).

### Steps

1. **Clone the Repository**

   Open your terminal or command prompt and execute:

   ```bash
   git clone https://github.com/yourusername/student-attendance-tracker.git
   cd student-attendance-tracker
   ```

2. **Install Dependencies**

   The application primarily uses standard Python libraries. However, ensure that Tkinter is installed (it usually comes pre-installed with Python).

   - **For Windows and macOS**: Tkinter is included with the standard Python installation.
   - **For Linux**: You might need to install it manually.

     ```bash
     sudo apt-get install python3-tk
     ```

3. **Verify Installation**

   Ensure that you have Python installed by checking the version:

   ```bash
   python --version
   ```

   or

   ```bash
   python3 --version
   ```

## Usage

Run the application by executing the main script.

```bash
python attendance_app.py
```

### Manage Students

1. **Navigate to the "Manage Students" Tab**

   ![Manage Students Tab](screenshots/manage_students.png)

2. **Add a New Student**

   - Enter a unique **Student ID** and the **Student Name**.
   - Click the **"Add Student"** button.
   - The student will appear in the list below.

   ![Add Student](screenshots/add_student.png)

3. **View Existing Students**

   The list below the input fields displays all added students with their IDs and names.

### Mark Attendance

1. **Navigate to the "Mark Attendance" Tab**

   ![Mark Attendance Tab](screenshots/mark_attendance.png)

2. **Enter the Date**

   - Input the date in `YYYY-MM-DD` format.
   - The current date is pre-filled by default.

3. **Load Students**

   - Click the **"Load Students"** button to display the list of students.
   - Existing attendance for the selected date will be loaded if available.

4. **Mark Attendance**

   - Select one or more students from the list.
   - Click **"Mark Present"** or **"Mark Absent"** to set their status.

5. **Save Attendance**

   - After marking, click **"Save Attendance"** to record the attendance.
   - A confirmation message will appear upon successful saving.

   ![Mark and Save Attendance](screenshots/mark_save_attendance.png)

### View Attendance

1. **Navigate to the "View Attendance" Tab**

   ![View Attendance Tab](screenshots/view_attendance.png)

2. **Choose View Option**

   - **View by Date**: See all students' attendance for a specific date.
   - **View by Student**: See a particular student's attendance history.

3. **View by Date**

   - Select the **"View by Date"** radio button.
   - Enter the desired date in `YYYY-MM-DD` format.
   - Click **"Load"** to display attendance records for that date.

4. **View by Student**

   - Select the **"View by Student"** radio button.
   - Choose a **Student ID** from the dropdown menu.
   - Click **"Load"** to view the student's attendance history.

   ![View Attendance by Date and Student](screenshots/view_options.png)

## Dependencies

- **Python 3.x**
- **Tkinter**: For creating the GUI. Included with Python on most platforms.
- **CSV**: Standard Python library for handling CSV files.
- **OS**: For file operations.
- **Datetime**: For handling date functionalities.

## File Structure

```
student-attendance-tracker/
├── attendance_app.py
├── students.csv
├── attendance.csv
├── README.md
└── screenshots/
    ├── manage_students.png
    ├── add_student.png
    ├── mark_attendance.png
    ├── mark_save_attendance.png
    └── view_options.png
```

- **attendance_app.py**: Main application script.
- **students.csv**: Stores student information (ID and Name).
- **attendance.csv**: Stores attendance records (Date, Student ID, Status).
- **README.md**: This readme file.
- **screenshots/**: Directory containing screenshots of the application (optional for visual guidance).

## Data Persistence

- **Students Data (`students.csv`)**:

  | ID    | Name           |
  |-------|----------------|
  | S001  | John Doe       |
  | S002  | Jane Smith     |
  | ...   | ...            |

- **Attendance Data (`attendance.csv`)**:

  | Date       | Student ID | Status  |
  |------------|------------|---------|
  | 2024-04-25 | S001       | Present |
  | 2024-04-25 | S002       | Absent  |
  | ...        | ...        | ...     |

- **File Initialization**: Upon first run, if `students.csv` or `attendance.csv` do not exist, the application creates them with appropriate headers.

## Input Validation

- **Unique Student IDs**: The application checks for duplicate Student IDs to maintain data integrity.
- **Date Format**: Ensures that dates are entered in the `YYYY-MM-DD` format.
- **Mandatory Fields**: Both Student ID and Name are required when adding a new student.

## Extensibility

This basic application can be extended with additional features such as:

- **Editing Student Details**: Modify existing student information.
- **Deleting Students**: Remove students from the database.
- **Exporting Reports**: Generate and export attendance reports in formats like PDF or Excel.
- **Authentication**: Add user login to secure the application.
- **Advanced UI**: Enhance the GUI with more sophisticated designs and functionalities.

Feel free to contribute and enhance the application to better suit your needs!

## License

This project is licensed under the [MIT License](LICENSE).

```
