from setuptools import setup

name = 'bolt'
version = '0.0.1a'
description = 	"""
This is a temporary description.
"""
author = 'Isaac Rodriguez'
author_email = 'isaac_rodriguez@live.com'
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
      author_email=author_email, 
      packages=packages,
      entry_points=entry_points)
