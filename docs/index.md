# Bolt Task Automation

[![Build](https://github.com/abantos/bolt/actions/workflows/build.yml/badge.svg)](https://github.com/abantos/bolt/actions/workflows/build.yml)
[![Release](https://github.com/abantos/bolt/actions/workflows/release.yml/badge.svg)](https://github.com/abantos/bolt/actions/workflows/release.yml)


Bolt is a task runner inspired by [grunt](http://gruntjs.com/) and written in
[Python](https://www.python.org) that helps you automate any task in your project
whether it is executed in your development environment or in your CI/CD pipeline.
Bolt gives you the power to specify how tasks should be executed, and it takes
care of the rest. And it is as simple as describing and configuring your tasks
in the `boltfile.py`.

```python
# boltfile.py

import bolt

config = {
    'pip': {
        'command': 'install',
        'options': {
            'r': './requirements.txt'
        }
    },
    'delete-pyc': {
        'sourcedir': './src',
        'recursive': True
    },
    'nose': {
        'directory': './tests',
        'options': {
            'with-xunit': True,
            'xunit-file': './logs/unit_test_log.xml'
        }
    }
}

bolt.register_task('run-tests', ['pip', 'delete-pyc', 'nose'])
```

```bash
# in your favorite shell

bolt pip
# to install requirements

bolt nose
# executes unit tests

bolt run-tests
# installs requirements, deletes .pyc files, and runs unit tests
```

## Why Use Bolt?

Let's face it, you want to automate everything, but doing so becomes a burden;
especially, if you are working on a cross-platform application. You may find
your-self switching CI/CD systems and going through the pain of
rewriting your pipelines to the specific domain languages they use. Python
is cross-platform and any pipeline will allow you to execute a command. This
makes Bolt ideal to create reusable tasks that can execute in any environment
independently of tools. And, It's fun!


## How Can I Get Started?

You can start by installing bolt and following the examples in the [Getting Started](using/getting_started.md) guide. Once you become familiar with Bolt, you can look at other topics in [Using Bolt](using_bolt.md) to learn about the different features it provides.


## This is Great! I want to Help!

Help is highly appreciated! If you want to contribute to the project, make sure
to read our [guidelines](contribute.md).
If you are a tool developer, and you want to provide Bolt support in your
library or application don't hesitate asking for help. We want to build a great
community around Bolt, and we will help you in any way we can.


Make sure you read the [bolt documentation](https://bolt-task-automation.readthedocs.io).
