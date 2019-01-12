#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='opsmop',
      version='0.1',
      description='Configuration management, application deployment, and orchestration system',
      author='Michael DeHaan',
      author_email='michael@michaeldehaan.net',
      license='Apache 2',
      url='https://opsmop.io/',
      packages=find_packages(exclude=['docs']),
      install_requires=[
          "PyYAML>=3.13",
          "toml>=0.10",
          "jinja2>=2.10",
          "dill>=0.2.8.2",
          "colorama>=0.4.1"
      ],
      dependency_links = [
          "git://github.com/dw/mitogen.git@1eb08fb5c5483fb7519893f65fb6a477c57045d1#egg=mitogen"
      ],
      zip_safe = False,
      classifiers = [
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: Apache Software License",
          "Natural Language :: English",
          "Operating System :: MacOS",
          "Operating System :: POSIX :: BSD",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3 :: Only",
          "System :: Systems Administration",
          "Topic :: System :: Operating System",
          "Topic :: Software Development :: Libraries"
      ]
)
