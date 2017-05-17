################################################################################
Creating Custom Tasks
################################################################################

The real power of Bolt is the ability to extend its functionality through new 
tasks that can be registered, configured, and executed through the ``boltfile.py``.
This section explains the different ways in which you can provide new tasks to 
bolt and some best practices that you should consider when creating your own 
tasks.

What is a Bolt Task 
================================================================================

A Bolt task is nothing but a Python callable object that will be invoked when 
its id is scheduled for execution. This means that to provide a new custom task
you need to implement the callable and register it with Bolt giving it a unique 
id, which can be used to invoke the task.

The :doc:`Getting Started <getting_started>` guide demonstrated this with a 
very simple example. Let's revisit it on its own for clarity:

..  code-block:: python 

    import bolt 

    def greeting(**kwargs):
        config = kwargs.get('config')
        message = config.get('message')
        print(message)


    bolt.register_task('greet', greeting)

    config = {
        'greet': {
            'message': 'Hello from Bolt!'
        }
    }


In this example, we implement our task right in the ``boltfile.py``. As you will
see later, the recommended way is to create your tasks in their own package or 
modules so you can re-use them, but this example will help us understand how
things work.

Right after the ``import`` statement, you have our task callable, which is a 
function that takes a set of keyword arguments (``**kwargs``). The function reads
the ``config`` argument and from it, it extracts the ``message`` we want to 
display.

The next step is to register the callable with Bolt, which is done by the call 
to ``bolt.register_task()``. We pass a unique identifier to our task and the 
callable that will be invoked.

Finally, we use the unique identifier for the task in our ``config`` to configure 
the message that we want to display.

As you can see, it is very simple to add a new custom task, but you will want to 
implement your tasks in a way that you can re-use them in different projects. 
The best way to do that is by creating your own modules or packages containing 
the Bolt tasks and then install them as requirements to the projects that use 
them. Let's take a look at that.


Implementing Custom Bolt Task Modules/Packages
================================================================================

Like any other python tool or application, you want to implement your Bolt tasks 
in their own modules or packages, so that you can install them as requirements 
in the projects you use them. The process to implement the tasks in a module 
is the same as above. The only difference is that you will have to provide a 
mechanism to register those tasks with Bolt, so they become available. Let's 
take a look at an example:

..  code-block:: python

    # in my_bolt_module.py 

    def greeting(**kwargs):
        config = kwargs.get('config')
        message = config.get('message')
        print(message)


    def register_tasks(registry):
        registry.register_task('greet', greeting)


As we discussed, the implementation stays the same, but we added a 
``register_tasks()`` function that takes a ``registry`` parameter, which 
allows us to make available the task to clients.

Now if someone wants to use our task, they can install the module and add it 
to the ``boltfile.py``:

..  code-block:: python 

    import bolt 
    import my_bolt_module 

    bolt.register_module_tasks(my_bolt_module)

    config = {
        'greet': {
            'message': 'Hello from Bolt!'
        }
    }

In this example, we first import the module containing the tasks, and then we 
register them by calling ``bolt.register_module_tasks()``. Bolt will create the 
``registry`` instance and pass it to the registration function in the module,
which will make the task available.

..  note::

    The ``bolt.register_task()`` function grabs the instance of the ``registry``
    and delegates to its method to register the task. Even-thought the result
    is the same, you should always use ``bolt.register_task()`` in your 
    ``boltfile.py`` and ``registry.register_task()`` in the ``register_task()``
    function of your custom modules.


Using a Callable Class to Implement Bolt Tasks
================================================================================

Bolt tasks are callable objects; therefore, you can implement your task in a 
callable class. The following example shows how to implement the ``greet`` task
in a callable class:

..  code-block:: python

    # in my_bolt_module.py 

    class GreetingTask(object):

        def __call__(**kwargs):
            config = kwargs.get('config')
            message = config.get('message')
            print(message)


    def register_tasks(registry):
        registry.register_task('greet', GreetingTask())


This example implements the same task, but it uses a callable class (a class
that implements a ``__call__()`` method) to implement the functionality. When 
the task is registered, we use a class instance as opposed to the function 
name as the callable registration. Other than that, the code is the same.

You may ask your-self why use a class when implementing a function is simpler. 
For very simple tasks, a function will work fine. When I started working on Bolt, 
most of the standard tasks were implemented as functions. Overtime, I reealize 
that classes will suit me better for the following reasons:

**Classes are more suitable for testing.** I write all my code using a TDD 
(Test Driven Development) process, and you should too. Unit testing functions 
that return a result is very simple, but testing functions with side-effects, it 
is a little bit more complicated. It didn't take long to see that most task were 
accessing external resources or code that will perform operations but will not 
return any useful values. In these cases, unit testing a function becomes very 
difficut, because it is hard to mock a specific state. Using a class makes unit
testing simpler because you can always set the class to a desired state.

**Classes simplify passing parameters.** In our examples, we are dealing with 
just one option in our configuration. As soon as you start supporting more 
configuration options, you have to deal with validation of those options and 
conditional code that depends of values of those parameters. Classes work a 
lot better because you can have internal implementation methods that can 
access those options as data members, as opposed to having to pass them as 
parameters to other functions. 

**Classes can keep alive resources after execution.** Imagine a task that needs
to start a web-server to make a service available, while subsequent tasks run 
tests against the server. This task will have to start the service in a separate
process and keep it running until the tests are done, but it will be nice to 
shut down the server once the test is complete. As we will see below, Bolt 
supports a ``tear_down()`` method that gets invoked at the end, and where 
resources can be freed. This can only be done with classes and not with functions.


The Execution Context
================================================================================

We have seen how to create new tasks and how support configuration options for
them. But once in a while, you will run into a situation where it will be nice 
to share some data or state among different tasks. In those situations, you can 
use the execution context object.

The execution context is a |python|_ dictionary like object where you can store
key/value pairs to share them with subsequent tasks. 

..  tip::

    The context object is a plain |python|_ dictionary that is passed to every
    task being executed, but this might change in the future, so you should 
    assume that the only available interface for this object is that of a 
    dictionary.

I am not a big fan of sharing data between tasks because it can create unwanted
dependencies among otherwise independent tasks, but I also recognize that it is 
a concept that may come handy in certain situations. In general, try to avoid 
task implementations that rely on certain properties available in the context 
object and always provide suitable defaults in case the properties are missing.
Let's take a look at a scenario where the execution context might come handy.

Assume we are writing a task that requires a job name from a service and doing
so, it is an expensive operation. Furthermore, there is group of tasks that 
will use that job name, so you want to retrieve it once and use it in all other 
tasks.

In a situation like this, we will write a task that retrieves the job name and 
stores it in the context object, so subsequent tasks can use it (I'm using
functions for simplicity, but I prefer classes).

..  code-block:: python

    # In my_job_tasks.py 

    def retrieve_job_name(**kwargs):
        config = kwargs.get('config')
        job_id = config.get('job-id')
        manager = JobManager()
        job = manager.get_job(job_id)   # Very expensive operation. 
        context = kwargs.get('context')
        context['job-name'] = job.name 


    def notify_job_name(**kwargs):
        config = kwargs.get('config')
        context = kwargs.get('context')
        job_name = config.get('job-name') or context.get('job-name')
        notifier = Notifier()
        notifier.notify_job_name(job_name)


    def register_tasks(registry):
        registry.register_task('retrieve-job', retrieve_job_name)
        registry.register_task('notify-job-name', notify_job_name)


As you can see, the ``retrieve_job_name`` task retrieves the job name and 
stores it in the context object. Then, the value is used by the
``notify_job_name`` task. Notice how we still try to retrieve the job name 
from the task ``config``. This allows to override that value in the
``boltfile.py`` which might come handy during testing.

..  tip::

    When implementing a task that relies on some information stored in the 
    context object, think about whether there is a suitable default or might be
    convenient to override the value through the configuration.

..  tip::

    Avoid creating dependencies between tasks by over-using the context object.
    However, you'll find that some times it is a very handy feature.

    
