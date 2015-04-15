# Copyright 2015 Vinicius Chiele. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading

from simplebus.local import Proxy

__bus = None
__local = threading.local()


def get_current_bus():
    return __bus


def get_current_message():
    if hasattr(__local, 'current_message'):
        return __local.current_message
    return None


def set_current_bus(bus):
    global __bus
    __bus = bus


def set_current_message(message):
    if message:
        __local.current_message = message
    else:
        del __local.current_message


current_bus = Proxy(get_current_bus)
current_message = Proxy(get_current_message)
