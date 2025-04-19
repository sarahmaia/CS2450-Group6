# Milestone5

## Description
A simulator where computer science students can execute their BasicML programs, providing a graphical interface to load and run BasicML files.

## Clone the repository
To clone the repository, use the following command:

```bash
git clone https://github.com/sarahmaia/CS2450-Group6.git
```

## Branches
This project contains multiple branches:

main: Base branch with milestone progress
Alan: Contains the tabbed GUI implementation for running multiple programs simultaneously, however it does not support for the requirements on Milestone 5
test: Most up-to-date and feature-complete branch. Use this for running and testing the program.

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
python3 -m src.Milestone5.gui.gui
python -m src.Milestone5.gui.gui

Once the GUI is open:

    Click the "Load Program" button.

    Navigate to and select a .txt file containing your BasicML program.

    Click "Run" to execute the program.

    Follow on-screen prompts for input and monitor output and memory in the interface.

    Use the "Change Colors" button to customize the GUI theme.

    Note: The GUI enforces a limit of 250 instructions and handles syntax errors.

    Note: The user is allow to modify the instructions panel.

    Note: The user is allowed to add more than 1 program, select the new tab button to add a new tab where a new program can be loaded without loosing the previous loaded program in the other tab or tabs.

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

This is milestone number five of the project. It includes:

    A refined, interactive GUI with improved layout and error handling

    Color customization stored in a config file (config.json)

    Program constraints such as instruction limits and error handling for invalid inputs

    Full separation of concerns between GUI and backend logic for easier maintenance and testing

    Instruction display is in binary format but the output is displayd in decimal

    Line numbers are removed from the instruction panel

    250 lines supported

    program with 4 digit and 6 digit words are supported

## Credits
Sarah Maia, Alan Hernandez, Jalal Khan, Santos Laprida

## Additional Notes
This is prototype number five of the project, which includes a color-customizable graphical user interface (GUI) with tkinter for loading and running BasicML programs.
