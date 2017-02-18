################################################################################
Disecting the Bolt File
################################################################################

The ``boltfile.py`` is the main script used by Bolt to execute the tasks which 
with it is invoked. The file contains the task definitions, as well as, the 
configuration parameters for the tasks. If you haven't done so
yet, review the :doc:`Getting Started <getting_started>` guide to familiarize 
your-self with a very basic example of a ``boltfile.py``. In this section, we 
will look at more advanced examples to learn the different features of Bolt. 

In essence, a Bolt File is just a |python|_ script. Within it, you can use the 
Bolt API to define and configure the tasks you want to execute. You can name the 
script whatever you want and place it in any location, but Bolt, by default, 
will look in the current working directory for a file named ``boltfile.py`` and 
use it if no other file is specified. This is the recommended way to work with 
Bolt.

..  code-block:: powershell

    # Assumes boltfile.py in the current working directory.
    bolt task-to-execute  

    # Uses specified file.
    bolt task-to-execute --bolt-file myboltfile.py  


..  tip::

    You can run ``bolt --help`` to see Bolt's usage and supported arguments.


The Structure of a Bolt File
================================================================================

There are three distinct sections in a ``boltfile.py``. The first section, like 
in any other |python|_ module is the imports, and your can bring in any module
you want. 

The second part is the registration of tasks. This involves registering custom 
task modules you want to use, as well as, defining custom tasks to create more 
complex execution workflows.

The third section of the ``boltfile.py`` is the configuration. Every Bolt File 
must declare a ``config`` variable set to a dictionary where the configuration 
parameters are defined. The dictionary can be empty, but it is required to
define the variable. Of course, an empty dictionary will not help us to do 
much.

The following shows the contents of the ``boltfile.py`` that we created in the 
:doc:`Getting Started <getting_started>` guide  and illustrates the three 
sections.

..  code-block:: Python 

    # Imports section 
    import bolt

    # Task registration section 
    bolt.register_task('run-tests', ['pip', 'delete-pyc', 'nose'])

    # Configuration section 
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

..  tip::

    It doesn't make any difference if you include your configuration before the 
    registration of tasks. As a matter of fact, I started doing it that way 
    myself because of the experience I had with |grunt|_. But my experience has 
    been that it makes the ``boltfile.py`` more readable if you register your 
    tasks right after the imports, and users can see the tasks available 
    immediately after opening the file. Overtime, your configuration will grow 
    with the usage of Bolt and users will have to scroll all the way down to 
    find the available tasks, which is, usually, the most important part of the 
    file.


The Import Section
================================================================================

The import section of the ``boltfile.py`` is no different than the imports in any
other python script or module. You will always need to import ``bolt`` to gain 
access to its API, which is used, among other things, to register tasks. You will
import and register other modules containing custom tasks. Finally, you can 
import any other libraries you might need.


The Task Registration Section 
================================================================================

There are different ways to define and register tasks with Bolt. In this section,
we will take a look at the different options and when we should use each one of 
them.

Bolt Provided Tasks 
-------------------

Bolt provides a set of tasks that are always available when executing Bolt. You 
don't need to register them because Bolt does that for you, and they 
can be configured without prior registration. This is the case for the tasks 
shown in the following example, which we will use as starting point.

..  code-block:: Python 

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


The tasks in the example (``pip``, ``delete-pyc``, and ``nose``) are provided by
Bolt; therefore, we don't need to register them to use them. With this simple
example you can still run each task independently to execute them. 

..  code-block:: powershell 

    # Install requirements 
    bolt pip 

    # Delete existing .pyc files 
    bolt delete-pyc 

    # Execute unit tests 
    bolt nose 


As you can see, it is very easy to leverage the existing functionality in Bolt, 
but the true power comes from the ability to define and create your own tasks 
or use other tasks provided by tool and library implementers. Let's take a look
at other ways to define tasks.


Composing Tasks From Existing Ones
----------------------------------

In the example above, we can use any of the three tasks provided by Bolt, but 
most of the time I will want to run all those tasks together. I want to make 
sure that when anyone working on my project gets source changes they can have 
the correct environment setup; therefore, I want them to install any required 
packages, and execute the tests with a clean run. For that I can define a 
composite task that will execute all three. The following shows the full contents
of the ``boltfile.py`` after adding the composite tasks.

..  code-block:: Python 

    import bolt

    bolt.register_task('run-tests', ['pip', 'delete-pyc', 'nose'])
    bolt.register_task('default', ['run-tests'])

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

We added two additional lines to our bolt file. The first one defines a 
composite task ``run-tests`` that execute the previous three. The second line 
registers a ``default`` task that executes the previously defined ``run-tests``.
Both of this tasks will execute the same set of steps.

Now, I can execute ``bolt run-tests`` from the command line to execute all tasks,
or I can simply call ``bolt``.

..  tip::

    The ``default`` task is a special task that gets executed when calling Bolt 
    without specifying a task to execute. You should always provide a ``default``
    task in your ``boltfile.py``.

..  tip::

    You want your ``default`` task to be compose of the steps you will execute 
    more often. I like to define ``default`` as the task that I will 
    always execute when I pull new changes from my central repo and before 
    publishing those changes, so I usually include steps to install new 
    required packages, clean the project tree, and execute the unit tests.


Registering Additional Modules 
------------------------------

As you start using Bolt more, you will find your-self implementing your own 
custom tasks or using modules provided by third-party libraries you use (see 
:doc:`Creating Custom Tasks <custom_tasks>` ). 
In order to use those tasks, you need to import the module containing them and 
register the module. The following example shows how can your register the tasks
in a custom or third-party provided module.

..  code-block:: Python

    # Removed contents for simplicity.
    import my_custom_tasks

    bolt.register_module_tasks(my_custom_tasks)


Now, all the tasks registered by ``my_custom_tasks`` become available for use 
and configure (see :doc:`Creating Custom Tasks <custom_tasks>` for more
information about how to create your own).


The Power of Configuration
================================================================================

Bolt provides a very powerful configuration mechanism that abstracts what the 
user wants to do from task implementers that expose configuration settings. This
means Bolt gives users the power to describe the configuration parameters of a 
task, and it takes care of resolving the configuration before it is sent to the 
task implementation, so that developers implementing tasks get a consistent set 
of configuration options.

To illustrate how Bolt processes configuration options, I will describe a  
scenario that I recently run into in one of my projects. 

In a recent project, I found myself using the ``awscli`` and ``boto3`` libraries
available for |python|_. Without going too much into the details of what I was 
doing, let's just say that I usually work on a Windows machine, but many of my 
applications and scripts are executed in Linux; therefore, cross-platform it is
very important for my projects (and one of the reasons why I choose |python|_).

Turns out that when you use ``awscli`` and/or ``boto3`` in Windows, you need to 
install an additional dependency called ``pypiwin32``. This dependency is not 
installed nor can be installed on Linux, so that simple fact threw me out for a 
few seconds on how I was going to manage the requirements for my project. 
Thankfully, I had Bolt at my disposal and I was able to fix the problem in a 
very simple, elegant way. 

The first step was to add ``awscli`` and ``boto3`` to my ``requirements.txt`` 
file. 

..  code-block:: text

    # In requirements.txt
    awscli>=1.11
    boto3>=1.4

Then, I created a second requirements file called ``requirements_win.txt`` and 
added the Windows specific library.

..  code-block:: text 

    # In requirements_win.txt 
    pypiwin32>=219


I still want all the people collaborating in my code to have the correct set of 
requirements, but I don't want them to have to worry about what they need to 
install because we use bolt for that. So, this is what I did in my bolt file:

..  code-block:: Python

    # Many lines removed for simplicity.

    import bolt 
    import sys 

    # Define a task to install the requirements.
    if sys.platform.startswith('win'):
        bolt.register_task('requirements', ['pip', 'pip.win']) # More on this below.
    else:
        bolt.register_task('requirements', ['pip'])


    bolt.register_task('run-tests', ['requirements', 'delete-pyc', 'nose'])
    bolt.register_task('default', ['run-tests'])


    config = {
        'pip': {
            'command': 'install',
            'options': {
                'r': 'requirements.txt'
            },
            'win': {
                'options': {
                    'r': 'requirements_win.txt'
                }
            }
        },
    }


This may seem more complicated than it really is once you understand how Bolt 
processes configurations, so let's take a look at it step by step. 

The first change I made was to check for the OS in which we are running and 
register a ``requirements`` task to install the requirements accordingly. Since,
the ``boltfile.py`` is just a |python|_ script, I can import ``sys`` and create 
conditional code if I want to. 

Now, let's take a look at what I do on Windows because it is something we haven't 
seen yet ``bolt.register_task('requirements', ['pip', 'pip.win']). What is this 
``pip.win`` thing? 

There might be times when I want to configure a task differently depending on the 
environment I'm running (I will show another example later, but this is so cool
that we will expain it first). In those circumstances, instead of providing a 
completely different ``boltfile.py`` with a different configuration, Bolt allows 
me to nest configuration options that I name my self.

The ``pip`` task knows nothing about the ``win`` option specified, and it doesn't 
have to worry about it, but when the ``pip`` task is invoked as ``pip.win``, Bolt
takes the configuration options for ``pip`` and then adds or overwrites any 
options defined in the nested ``win`` configuration. Therefore, the configuration 
passed to the ``pip`` task when called as ``pip.win`` will look like the following:

..  code-block:: Python

    config = {
        'commmand': 'install',  # Taken from parent
        'options': {
            'r': 'requirements_win.txt'
        }
    }

When the task is invoked as ``pip``, the configuration passed is:

..  code-block:: Python

    config = {
        'commmand': 'install',  # Taken from parent
        'options': {
            'r': 'requirements.txt'
        }
    }


In the registration of the ``requirements`` task for Windows, we execute both, 
where if we run on Linux we just execute ``pip``.

..  tip::

    You can nest configurations as deep as you want, so it will be possible to 
    define tasks as ``pip.win.32`` and ``pip.win.64`` if needed. In my experience,
    one level of nesting is what you will need for most practical cases, and it 
    keeps the configuration readable. 


A More Common Configuration Example 
-----------------------------------

The previous example is pretty cool, and it solve a very real problem, but most 
of the time you will not need or want to have a lot of conditional code in your 
``boltfile.py``. The following scenario illustrates a more common approach to 
define and configure tasks differently for different environments.

Many times I find my self wanting to execute a task differently when I run it in
my local development environment than when that task is running in the CI/CD 
pipeline for my project. A very common scenario for all my projects is that when 
I run the unit tests locally, which I do all the time, I run them with bare 
options, so I configure the task in the same way as the examples above.

During the build process, however, I want to get more information about the
execution of the tests, and I want to produce some reports and post them to my 
CI/CD system. Usually, I want a tests results report, and a code coverage 
report. The following shows the tasks I normally register and configure to 
execute the unit tests in the different environments.

..  code-block:: Python 

    # Lines omitted for simplicity.

    # Developer's tasks. I like to keep the names short, to type less when 
    # I run them.
    #
    bolt.register_task('ut', ['pip', 'delete-pyc', 'nose'])

    # Ci/CD Tasks 
    #
    bolt.register_task('run-tests', ['pip', 'nose.ci'])

    config = {
        # Again, lines omitted for simplicity.

        'nose': {
            'directory': './tests',
            'ci': {
                'options': {
                    'with-xunit': True,
                    'xunit-file': os.path.join('output', 'unit_tests_log.xml'),
                    'with-coverage': True,
                    'cover-erase': True,
                    'cover-package': './source',
                    'cover-branches': True,
                    'cover-html': True,
                    'cover-html-dir': os.path.join('output', 'coverage')
                }
            }
        }
    }

When I'm working on the project, I execute ``bolt ut``, which does all the 
operations I want in my local development environment. In CI/CD, I execute 
``bolt run-tests``, which runs different tasks, but I want you to focus on the 
different options that I use with ``nose``.

Without using any conditional code in the ``boltfile.py` itself, I can run
``nose`` in different ways by specifying a nested configuration ``ci``.

..  tip::

    If you look at the options set for ``nose.ci``, you can see that I use 
    ``os.path.join()`` to resolve the location where reports will be generated.
    This illustrates the power of configuration as code.



