################################################################################
Getting Started with Bolt
################################################################################

This section covers the basic topics to start using Bolt in your projects, from
the installation of Bolt, to creating your first bolt file, to configuring and
executing tasks using bolt.


Installing Bolt
===============

Unfortunately, I have not completed the work to publish Bolt and deliver it 
through ``pip``. This work should be completed soon, and then you can use that
mechanism to install it. For now, you can get the source from the |repo|_.

..  todo:: Complete the Installing Bolt section once we have pip integration.


Your First Bolt File (boltfile.py)
==================================

The bolt file is the basic element, other than bolt it-self, in any project
that intends to use Bolt. Bolt uses the file to configure and execute the 
defined automated tasks, and every aspect of the execution is provided in the
bolt file. The bolt file is nothing but a python script that uses some
conventions and provided functions to indicate how the automated tasks should
be executed.

By default, bolt will look for a `boltfile.py` file in the current working
directory and will use that file to execute the tasks. A different bolt file
can be used by specifying it as a command line argument (using the ``--bolt-file`` 
switch).

The bolt file is a python script that it is divided into three different sections.
The first one is the configuration section where a configuration is provided that
defines the parameters used with tasks. The second section is used to register
3rd-party or self-provided tasks. Finally, the third section will describe the
steps for each of the tasks that will be used by the project.

Bolt does not enforce the order of this tasks, but the bolt file is a python
script that will be executed with your |python|_ interpreter; therefore, it
must adhere to the |python|_ language, which requires things to be defined
before they can be invoke. You should followw the guidelines describe here
and structure your bolt files following those guidelines.

To illustrate the different sections and how they are used, we will start by
automating the task of clearing all the generated compiled python modules
from our project. As you know, python compile modules are generated as our
program is executed (``.pyc`` files), but in a developmenet environment, these
file may create some conflicts and cause unexpected behavior if we rename or
move modules, and we do not perform a clean-up. The task will automate this
process.

Start by creating a ``boltfile.py`` at the root of your project. We will use
this file to illustrate how Bolt is used.


Configuing Bolt Tasks
---------------------

The first element in the bolt file should be the configuration section. This
section is nothing but a python dictionary named ``config`` that includes the
configuration parameters to the tasks we intend to use with bolt. In the
file you created in the previous section (your ``boltfile.py``), add a ``config``
variable and set it to an empty dictionary. ::

    config = {}

..  note::

    The ``config`` variable is required since the Bolt application will
    try to read it; therefore, the variable must be declared even if we do
    not intend to configure our tasks. Bolt also expects it to be a dictionary,
    so you should declare it as an empty dictionary if you do not intend to
    use it.

Bolt provides a task that allows to delete ``.pyc`` files in a project. The
task gives a lot of flexibility as which files should be deleted, but for this
example, we will configure the task to search the entire project tree recursively
and delete all the ``.pyc`` files that it finds. Modify the previously defined
``config`` dictionary to include the ``delete-pyc`` task and its configuration
parameters as shown here::

        config = {
            "delete-pyc": {
                "sourcedir": "./",
                "recursive": True
            }
        }

The contents of the configuration should be self-explanatory, but let's take a
look at what each of the items and their rational.

The first thing we see is another dictionary declared underneath the main ``config``
dictionary with a key of ``"delete-pyc"``. The ``"delete-pyc"`` string is the
unique identifier of the provided task that deletes the ``.pyc`` files. What we
are saying in the example is used the following parameters specified in this
dictionary to customize the ``delete-pyc`` task.

The parameters to the task are task specific. Each task defines its own supported
parameters, their meaning, and how they should be defined and used. In our case,
we are providing a ``sourcedir`` of the current working directory, and we are
stating that we want to delete ``.pyc`` files recursively.

..  todo::  Include links to more advance configuration topics.

 
