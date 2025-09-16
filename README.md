# Readarr Replica

This is a simple replica of Readarr, a book collection manager. It's a web application built with Python and Flask.

## Running from Source

You can run this application directly from the source code. This is useful for development or if you don't want to build the executable.

1.  **Prerequisites:**
    *   Make sure you have Python and pip installed.

2.  **Set up the project:**
    *   Open **Command Prompt** or **PowerShell** and navigate to the project directory.
    *   Create a virtual environment:
        ```
        python -m venv venv
        ```
    *   Activate the virtual environment:
        ```
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    *   Install the required packages:
        ```
        pip install -r requirements.txt
        ```

4.  **Initialize the database:**
    *   Set the `FLASK_APP` environment variable:
        *   In **Command Prompt**: `set FLASK_APP=run.py`
        *   In **PowerShell**: `$env:FLASK_APP = "run.py"`
    *   Run the database migration to create the tables:
        ```
        flask db upgrade
        ```

5.  **Run the application:**
    *   In the same terminal, run the application:
        ```
        flask run
        ```
    *   The application will be available at `http://127.0.0.1:5000`.

## Building the Executable (for Windows)

You can build a standalone Windows executable (`.exe`) from the source code. This allows you to run the application without needing to have Python or any dependencies installed (on the target machine).

1.  **Follow steps 1-3 from "Running from Source"** to set up the project and install the dependencies. This includes installing `PyInstaller`.

2.  **Run the build script:**
    *   In the project's root directory, you will find a `build.bat` file. Double-click this file to run it.
    *   This script will run PyInstaller and create the executable.

3.  **Find the executable:**
    *   After the build script finishes, you will find a new `dist` folder. Inside this folder, you will find `run.exe`. This is your application.

## Running the Executable

1.  Navigate to the `dist` folder.
2.  Double-click `run.exe` to start the application.
3.  A web server will start in the background. Open your web browser and go to `http://127.0.0.1:5000` to use the application.
4.  The application's database file (`app.db`) will be created in the same `dist` folder.
