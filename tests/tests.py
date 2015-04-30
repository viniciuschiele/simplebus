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

import uuid

from simplebus import Bus
from simplebus import Config
from simplebus import current_message
from simplebus import MessageHandler
from simplebus import pull
from simplebus import subscribe
from threading import Event
from unittest import TestCase


class TestConfig(TestCase):
    def test_default(self):
        config = Config()
        self.assertEqual('amqp://guest:guest@localhost/', config.endpoints.get('default'))

    def test_from_object(self):
        config = Config()
        config.from_object(self.CustomConfig())
        self.assertEqual('amqp://test:test@localhost/', config.endpoints.get('default'))

    class CustomConfig(object):
        SIMPLEBUS_ENDPOINTS = {
            'default': 'amqp://test:test@localhost/'
        }


class TestPuller(TestCase):
    queue = 'tests.queue1'

    def setUp(self):
        self.bus = Bus()
        self.bus.start()

    def tearDown(self):
        self.bus.stop()

    def test_consumer_as_class(self):
        event = Event()

        class Handler1(MessageHandler):
            def handle(self_, message):
                self.assertEqual('hello', message)
                event.set()

        self.bus.pull(self.queue, Handler1())
        self.bus.push(self.queue, 'hello')

        event.wait()

    def test_pull_as_decorator(self):
        event = Event()

        @pull(self.queue)
        def handle(message):
            self.assertEqual('hello', message)
            event.set()

        self.bus.push(self.queue, 'hello')

        event.wait()

    def test_pull_as_function(self):
        event = Event()

        def handle(message):
            self.assertEqual('hello', message)
            event.set()

        self.bus.pull(self.queue, handle)
        self.bus.push(self.queue, 'hello')

        event.wait()

    def test_cancel(self):
        def handle(message):
            pass

        cancellation = self.bus.pull(self.queue, handle)
        cancellation.cancel()

    def test_max_delivery_count(self):
        event = Event()

        key = str(uuid.uuid4())

        def handle(message):
            raise RuntimeError('error')

        def handle_error(message):
            self.assertEqual(key, message)
            event.set()

        self.bus.pull(self.queue, handle, retry_delay=0)
        self.bus.pull(self.queue + '.error', handle_error, dead_letter_enabled=False, max_retry_count=0)
        self.bus.push(self.queue, key)

        event.wait()


class TestSubscriber(TestCase):
    topic = 'tests.topic1'

    def setUp(self):
        self.bus = Bus()
        self.bus.start()

    def tearDown(self):
        self.bus.stop()

    def test_subscriber_as_class(self):
        event = Event()

        class Handler1(MessageHandler):
            def handle(self_, message):
                self.assertEqual('hello', message)
                event.set()

        self.bus.subscribe(self.topic, Handler1())
        self.bus.publish(self.topic, 'hello')

        event.wait()

    def test_subscriber_as_decorator(self):
        event = Event()

        @subscribe(self.topic)
        def handle(message):
            self.assertEqual('hello', message)
            event.set()

        self.bus.publish(self.topic, 'hello')

        event.wait()

    def test_subscriber_as_function(self):
        event = Event()

        def handle(message):
            self.assertEqual('hello', message)
            event.set()

        self.bus.subscribe(self.topic, handle)
        self.bus.publish(self.topic, 'hello')

        event.wait()

    def test_unsubscribe(self):
        def handle(message):
            pass

        subscription = self.bus.subscribe(self.topic, handle)
        subscription.cancel()
