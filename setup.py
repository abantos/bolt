from setuptools import setup
import bolt.about

name = bolt.about.project
version = bolt.about.release
description = 	bolt.about.description
author = bolt.about.author

packages = ['bolt']
entry_points = {
    'console_scripts': [
        'bolt = bolt:run'
    ]
}

setup(name=name,
      version=version,
      description=description,
      author=author,
      packages=packages,
      entry_points=entry_points)
