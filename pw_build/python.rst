.. _module-pw_build-python:

-------------------
Python GN templates
-------------------
The Python build is implemented with GN templates defined in
``pw_build/python.gni``. That file contains the complete usage documentation.

.. seealso:: :ref:`docs-python-build`

pw_python_package
=================
The main Python template is ``pw_python_package``. Each ``pw_python_package``
target represents a Python package. As described in
:ref:`module-pw_build-python-target`, each ``pw_python_package`` expands to
several subtargets. In summary, these are:

- ``<name>`` - Represents the files themselves
- ``<name>.lint`` - Runs static analysis
- ``<name>.tests`` - Runs all tests for this package
- ``<name>.install`` - Installs the package
- ``<name>.wheel`` - Builds a Python wheel

Arguments
---------
- ``setup`` - List of setup file paths (setup.py or pyproject.toml & setup.cfg),
  which must all be in the same directory.
- ``sources`` - Python sources files in the package.
- ``tests`` - Test files for this Python package.
- ``python_deps`` - Dependencies on other pw_python_packages in the GN build.
- ``python_test_deps`` - Test-only pw_python_package dependencies.
- ``other_deps`` - Dependencies on GN targets that are not pw_python_packages.
- ``inputs`` - Other files to track, such as package_data.
- ``lint`` - If true (default), applies Mypy and Pylint to the package. If
  false, does not.
- ``pylintrc`` - Optional path to a pylintrc configuration file to use. If not
  provided, Pylint's default rcfile search is used. Pylint is executed
  from the package's setup directory, so pylintrc files in that directory
  will take precedence over others.
- ``mypy_ini`` - Optional path to a mypy configuration file to use. If not
  provided, mypy's default configuration file search is used. mypy is
  executed from the package's setup directory, so mypy.ini files in that
  directory will take precedence over others.

Example
-------
This is an example Python package declaration for a ``pw_my_module`` module.

.. code-block::

  import("//build_overrides/pigweed.gni")

  import("$dir_pw_build/python.gni")

  pw_python_package("py") {
    setup = [ "setup.py" ]
    sources = [
      "pw_my_module/__init__.py",
      "pw_my_module/alfa.py",
      "pw_my_module/bravo.py",
      "pw_my_module/charlie.py",
    ]
    tests = [
      "alfa_test.py",
      "charlie_test.py",
    ]
    python_deps = [
      "$dir_pw_status/py",
      ":some_protos.python",
    ]
    python_test_deps = [ "$dir_pw_build/py" ]
    pylintrc = "$dir_pigweed/.pylintrc"
  }

pw_python_script
================
A ``pw_python_script`` represents a set of standalone Python scripts and/or
tests. These files support all of the arguments of ``pw_python_package`` except
those ``setup``. These targets can be installed, but this only installs their
dependencies.

pw_python_group
===============
Represents a group of ``pw_python_package`` and ``pw_python_script`` targets.
These targets do not add any files. Their subtargets simply forward to those of
their dependencies.

pw_python_wheels
================
Builds and collects Python wheels for one or more ``pw_python_package`` targets.
A package's ``.wheel`` subtarget builds the wheel for just that package.
``pw_python_package`` collects wheels from all of its transitive dependencies
and collects them in a specified directory.

pw_python_requirements
======================
Represents a set of local and PyPI requirements, with no associated source
files. These targets serve the role of a ``requirements.txt`` file.