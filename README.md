# Data manager



## Adding new python packages to the project

This project uses pip-tools to manage requirements files. [https://pypi.org/project/pip-tools/](https://pypi.org/project/pip-tools/)

When using fresh checkout of this repository, then make init will take care of the initial of packages from the checked
in requirements and dev-requirements files. 

These instructions are only for when you add new libraries to the project.

To add a production dependency to the main aapplication, add the package to [requirements.in](requirements.in)

    python -m piptools compile requirements/requirements.in

That will generate a new requirements.txt file

To add a development library, add a line to [dev-requirements.in](dev-requirements.in). Note that the first line of that file is:
"-c requirements.txt" which constrains the versions of dependencies in the requirements.txt file generated in previous step.

    python -m piptools compile requirements/dev-requirements.in

Then run

    python -m piptools sync requirements/requirements.txt requirements/dev-requirements.txt