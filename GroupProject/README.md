# Milestone4

## Description
A simulator where computer science students can execute their BasicML programs, providing a graphical interface to load and run BasicML files.

## Clone the repository
To clone the repository, use the following command:

```bash
git clone https://github.com/sarahmaia/CS2450-Group6.git
```

## Installation
To install the project, ensure Python is installed and required dependencies are available. 

See [Installation](docs/installation.rst) for more details.

## Usage
Navigate to the root project directory:

```bash
cd GroupProject
```

Run the program:

```bash
python3 -m src.Milestone4.gui.gui
python -m src.Milestone4.gui.gui
```
Once the GUI is open:

    Click the "Load Program" button.

    Navigate to and select a .txt file containing your BasicML program.

    Click "Run" to execute the program.

    Follow on-screen prompts for input and monitor output and memory in the interface.

    Use the "Change Colors" button to customize the GUI theme.

    Note: The GUI enforces a limit of 100 instructions and handles syntax errors.

    Note: The the user is allow to modify the instructions panel.

## Tests
Navigate to the root project directory:

```bash
cd GroupProject
```

Execute the unit tests:

```bash
python3 -m tests.testUVSim
```
## Additional Notes

This is the fourth milestone of the project. It includes:

    A refined, interactive GUI with improved layout and error handling

    Color customization stored in a config file (config.json)

    Program constraints such as instruction limits and error handling for invalid inputs

    Full separation of concerns between GUI and backend logic for easier maintenance and testing

## Credits
Sarah Maia, Alan Hernandez, Jalal Khan, Santos Laprida

## Additional Notes
This is the third prototype of the project, which includes a color-customizable graphical user interface (GUI) with tkinter for loading and running BasicML programs.
