# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import json
import os
import shlex

import toml
import yaml

# while we want to keep this miminal, the common class contains some useful functions usable by many providers.

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def memoize(func):
    """
    The second time the decorated function is called, return the previous response value
    versus calling the function.
    """
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func

def shlex_kv(msg):
    data = shlex.split(msg)
    results = dict()
    for item in data:
        if '=' in item:
            (k,v) = item.split("=",1)
            results[k] = v
        else:
            raise Exception("invalid input: %s" % data)
    return results

def load_data_file(path):
    path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    if not os.path.exists(path):
        raise Exception("path does not exist: %s" % path)
    if path.endswith(".toml"):
        return toml.load(path)
    elif path.endswith(".json"):
        fd = open(path)
        return json.loads(fd.read())
    elif path.endswith(".yaml"):
        fd = open(path)
        data = yaml.safe_load(fd.read())
        return data
    else:
        raise Exception("unknown extension: %s" % path)
