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

import concurrent


class Batch(object):

    def __init__(self, hosts, batch_size=10):
        if type(hosts) == dict:
            hosts = hosts.values()
        self.hosts = [ h for h in hosts ]
        self.batch_size = batch_size

    def next(self):
        results = []
        for x in range(0, self.batch_size):
            if len(self.hosts) == 0:
                return results
            results.append(self.hosts.pop())
        return results

    def apply_async(self, fn, max_workers=8):
        
        while True:

            batch = self.next()
            if len(batch) == 0:
                return

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for host in batch:
                    futures.append(executor.submit(fn, host))
                for future in concurrent.futures.as_completed(futures):
                    try:
                        data = future.result()
                    except Exception as exc:
                        raise


    def apply(self, fn):

        while True:
            batch = self.next()
            if len(batch) == 0:
                return
            for host in batch:
                fn(host)
