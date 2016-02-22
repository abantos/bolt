################################################################################
Bolt's User Guide
################################################################################

You've decided to use Bolt in your project (or maybe just try it out to see 
what it can do for you). Great! This is a great place to start. This section
will show you how to get started with Bolt and what it can do for you.

..  todo::  This may have to be a tutorial with more in deep topics in other
            documents.


Installing Bolt
===============

Unfortunately, I have not completed the work to publish Bolt and deliver it 
through ``pip``. This work should be completed soon, and then you can use that
mechanism to install it. For now, you can get the source from the |repo|_.

..  todo:: Complete the Installing Bolt section once we have pip integration.


Creating the Bolt File
======================

The Bolt file (``boltfile.py`` by default) is where the tasks are defined,
registered, and configured. Bolt uses this file to determine which task to
execute and the configuration to be used. As with |grunt|_, the file is
divided into three logical sections, and it is recommended that the
definitions in the file follow this structure.

The Configuration Section
-------------------------

At the top of the Bolt file, you must create a ``config`` variable set to
a python dictionary that will serve as configuration. The variable does not
have to be declared at the top, and in fact, it can exist anywhere in the file, 
but it is required, and it is a good idea to have it at the top after other 
module imports. ::

    # In boltfile.py

    config = {
        "my-task": {
            "option": "value"
        }
    }

The structure of the configuration is straight-forward. There is an encompassing
python dictionary that contains the configuration for all tasks that will
be used or defined in the bolt file. Each task configuration is an entry
in the top-level dictionary where the key is the task name/id and the value
is another dictionary containing the configuration parameters and values.

In the example above, we can assume that there is a task named ``my-task``, and
the defined dictionary will be passed as confguration. Bolt does not verify the
contents of the task configuration (it can't since it doesn't know what the 
task does), so it is up to the task implementer to do any validation.

Bolt provides a flexible mechanism to define task configurations. A task might
require diffent parameters depending on what it is being done.
