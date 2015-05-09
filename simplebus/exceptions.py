# Copyright 2015 Vinicius Chiele. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains all exceptions used by the SimpleBus API."""


class SerializationError(Exception):
    """Serialize or Deserialize has failed."""

    def __init__(self, message):
        self.message = message


class SerializerNotFoundError(Exception):
    """Serializer not found."""

    def __init__(self, message):
        self.message = message