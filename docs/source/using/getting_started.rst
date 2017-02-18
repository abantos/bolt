################################################################################
Getting Started
################################################################################

In this section, we will take a look at some of the basics by installing Bolt
and creating an initial ``boltfile.py`` to learn the main concepts.


Installing Bolt
================================================================================

Bolt can be installed directly from PyPi using pip.

..  code-block:: powershell

    pip install bolt-ta



Your First Bolt File
================================================================================

A Bolt file (``boltfile.py``) is just a |python|_ script that defines the tasks
available and the configuration for each of those tasks. Once we have a Bolt 
file for our project, we can run the available tasks at any time. In this 
section, we will learn the basics of the Bolt file by creating one that defines
a very common scenario: First, it will run a task to install any missing 
requirements for the application (basically a ``pip install``). Then, it will 
clean all the ``.pyc`` files out of the source tree to insure a clean state. 
After that, it will execute all the unit tests. And finally, we will add a
greeting message at the begining of our tasks just to demonstrate how to create
a simple custom task.

Let's begin by looking at the structure for a our sample python project. The 
following shows the contents of the root directory (simplified for clarity):

..  code-block:: powershell

    - project-root 
        |- source
        |- tests
        |- requirements.txt
        |- boltfile.py


Installing Requirements
-----------------------

We will start by creating a ``boltfile.py`` file at the root of our project as
shown in the structure above. Once the file is created, we will create a 
configuration object inside the file to point to our requirements file, which 
contains the requirements of our application. The initial contents of 
``boltfile.py`` look like the following:

..  code-block:: python

    import bolt

    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': 'requirements.txt'
            }
        }
    }


You can now run ``bolt pip`` from the command line and see how the specified
requirements are installed. In my example, the ``requirements.txt`` file only
lists the ``requests`` module:

..  code-block:: shell

    (btsample) D:\Projects\Playground\bolt-sample> bolt pip
    INFO - Executing Python Package Installer
    Collecting requests (from -r requirements.txt (line 1))
    Using cached requests-2.13.0-py2.py3-none-any.whl
    Installing collected packages: requests
    Successfully installed requests-2.13.0
    (btsample) D:\Projects\Playground\bolt-sample>


Let's go over the example to understand what's going on. When bolt is executed 
in a directory containing a ``boltfile.py``, the file is loaded as any other
python module. Bolt requires the ``boltfile.py`` to define a ``config`` variable
that is set to a configuration object, which is nothing but a |python|_ 
dictionary. The root keys in the dictionary (in our case ``pip``) are the id of 
the tasks we want to configure. Turns out Bolt provides a set of out-of-the-box
tasks that can be used without any further process, and one of them is ``pip``.

The ``pip`` task requires to specify a command to execute. In our sample we use 
the ``install`` command, but you can use any command supported by the actual 
``pip`` package Installer. The ``install`` allows to specify a requirements 
file. In our example, we set the ``r`` option to the file containing the
requirements (``requirements.txt``). If you think about it, all we are doing 
is invoking ``pip install -r requirements.txt``, which is what you will 
normally use from the command line, but Bolt is taking care of invoking the 
command for us (see :ref:`pip task documentation <task-pip>`
for more information about how to use the task).

Because the ``pip`` task is provided out-of-the-box, we do not need to register
it with Bolt, so we can just execute it from the command line by invoking
``bolt pip``.


Cleaining PYCs and Executing Unit Tests 
---------------------------------------

Before we run our unit tests, we want to clear any ``.pyc`` files that have been
generated from a previous run. Bolt provies a task (``delete-pyc``) to do just
that and it can be configured as follows:

..  code-block:: python

    import bolt

    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': 'requirements.txt'
            }
        },
        'delete-pyc': {
            'sourcedir': './source',
            'recursive': True
        }
    }


As you can see, the configuration of the ``delete-pyc`` task is self-explanatory.
The task will search the ``sourcedir`` specified for ``.pyc`` files and it 
will delete them. Because we specified the ``recursive`` option, it will also 
search the entire directory tree under ``source`` and delete all the matches
(for more information see the :ref:`delete-pyc task documentation <task-delete-pyc>` ).


Let's not stop there! We don't want to just delete the ``.pyc`` files, we also
want to execute the unit tests. In my example, I use ``nose`` as the test 
runner since Bolt already provides a task for that. Let's take a look at the 
updated ``boltfile.py``:

..  code-block:: python

    import bolt

    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': 'requirements.txt'
            }
        },
        'delete-pyc': {
            'sourcedir': './source',
            'recursive': True
        },
        'nose': {
            'directory': 'tests'
        }
    }

    bolt.register_task('run-tests', ['pip', 'delete-pyc', 'nose'])


We added nose to the configuration, which just uses a ``directory`` parameter 
that points to the location of the tests (see the :ref:`nose task documentation <task-nose>` 
for more information). But, we also added the following line
at the end: ``bolt.register_task('run-tests', ['pip', 'delete-pyc', 'nose'])``.
Let's take a look at what that does.

The ``run-tests`` task, which we are defining, is composed of the three 
other tasks that we have configured. These tasks will be executed sequentially
when the ``run-tests`` task is invoked by invoking Bolt as ``bolt run-tests``.
We can additionally run ``bolt delete-pyc`` to just delete the ``.pyc`` files, 
run ``bolt nose`` to just run the unit tests, and of course ``bolt pip`` as we 
saw before.

Bolt will take care of executing the task you provide and insuring the correct
configuration is passed to the task. It will also handle and report errors
and stop execution if there are any problems, so the problems can be fixed.


Display a Greeting When Bolt Runs
---------------------------------

Bolt provides a set of tasks that can be used as soon as you install it, but 
it also allows you to add other tasks that are specific to your project.
Furthermore, tool makers can provide their own tasks to integrate Bolt with 
their applications and libraries. To demonstrate how easy is to create a Bolt 
task, we will provide one that displays a greeting at the begining of the 
``run-tests`` task. Let's take a look at the implementation, and then, we'll 
discuss it.

..  code-block:: python

    import bolt

    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': 'requirements.txt'
            }
        },
        'delete-pyc': {
            'sourcedir': './source',
            'recursive': True
        },
        'nose': {
            'directory': 'tests'
        },
        'greet': {
            'message': 'Welcome to Bolt!'
        }
    }


    def greet_task(**kwargs):
        config = kwargs.get('config')
        message = config.get('message')
        print(message)


    bolt.register_task('greet', greet_task)
    bolt.register_task('run-tests', ['greet', 'pip', 'delete-pyc', 'nose'])


We first added a configuration key ``greet`` for our task. This is the id we 
chose for the task, and we will also use it to register it with Bolt. The 
configuration takes a ``message`` option, which value is the message we want to 
display. 

Then we added a new function ``greet_task``, which is the callable object that 
Bolt will call when the task is invoked. The funtion receives a keyword 
arguments object, which contains a ``config``, which value is the configuration
we defined. The function retrieves the configuration and reads the message from
it in order to display it. Notice that the value of the ``config`` keyword 
argument is not the entire configuration; it just contains the parameters
related to our task, in other words the value is:

..  code-block:: python 

    {
        'message': 'Welcome to Bolt!'
    }

Once we have the function and its configuration, we register it by calling
``bolt.register_task('greet', greet_task)`` where the first parameter is the id 
of our task, which we also used for the configuration, and the second parameter 
is the callable we want to execute, in our case the function ``greet_task``. 
Finally, we put our greet task at the beginning of ``run-tests`` and we will 
see the message when we execute it.

That's it! You can run ``bolt greet`` to just see the message, or you can 
execute ``bolt run-tests`` and see the message followed by the other tasks.



