====================================================
(Milestone3) Installation
====================================================

macOS:
------

Ensure Python is installed:

.. code-block:: bash

   python3 --version

If Python is not installed, install it using Homebrew:

.. code-block:: bash

   brew install python

Windows:
--------

Ensure Python is installed:

.. code-block:: bash

   python --version

If Python is not installed, install it via Windows Package Manager:

.. code-block:: bash

   winget install Python.Python

Linux:
------

Ensure Python is installed:

.. code-block:: bash

   python3 --version


If Python is not installed, install it using the following commands based on your distribution:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Debian/Ubuntu:
^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt update && sudo apt install python3

Fedora:
^^^^^^^

.. code-block:: bash

   sudo dnf install python3

Arch Linux:
^^^^^^^^^^^

.. code-block:: bash

   sudo pacman -S python

Ensure unittest is available:
-----------------------------

.. code-block:: bash

   python -m unittest --help

Ensure tkinter is available:
----------------------------

.. code-block:: bash

   python -c "import tkinter; print('tkinter is available')"

If available, you should see:

.. code-block:: bash

   tkinter is available


