# External deips
import pdb
from threading import Lock
from typing import Callable

import json
import logging
import pika
import sys
import threading

LOG = logging.getLogger(__name__)
_TERMINATION_SIGNAL = "SOMEBODY KILL ME!"


class EventListener(object):

    def __init__(self, queue_name: str):
        super(EventListener, self).__init__()

        LOG.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        LOG.addHandler(ch)

        self._events = {}
        self._connection = None
        self._channel = None
        self._consumer_tag = None
        self._consumer_thread = None
        self._queue_name = queue_name

    def add_listener(self, event_name: str, callback: Callable):
        LOG.debug("Registered a listener for {}".format(event_name))
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def remove_listener(self, event_name: str, callback: Callable):
        LOG.debug("Removed a listener for {}".format(event_name))
        if event_name in self._events and callback in self._events[event_name]:
            self._events[event_name].remove(callback)

    def start(self):
        self._consumer_thread = threading.Thread(target=self._start)
        self._consumer_thread.start()

    def stop(self):
        # Since the pika connection can't be safely used across threads,
        # tell the server thread to stop consuming.
        # Also, since threads can't join themselves, do that here too when the server
        # has been stopped
        temp_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        temp_channel = temp_connection.channel()
        term_msg = json.dumps({_TERMINATION_SIGNAL: ""})
        temp_channel.basic_publish("", self._queue_name, term_msg)
        self._consumer_thread.join()

    def _stop(self):
        self._channel.stop_consuming(self._consumer_tag)
        self._channel.basic_cancel(self._consumer_tag)

    def _on_channel_canceled(self, _):
        self._connection.close()

    def _start(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self._channel = self._connection.channel()
        self._channel.queue_declare(self._queue_name)
        self._consumer_tag = self._channel.basic_consume(
                self._queue_name, self._event_handler, auto_ack=True)
        self._channel.add_on_cancel_callback(self._on_channel_canceled)
        self._channel.start_consuming()

    def _event_handler(self, channel, method, properties, body):
        msg_obj = json.loads(body.decode('utf-8'))
        event_name = list(msg_obj.keys())[0]

        if event_name == _TERMINATION_SIGNAL:
            LOG.debug("Received termination signal")
            self._stop()
            return

        if event_name not in self._events:
            LOG.debug("Received event {}, but nobody is listening for it"
                      .format(event_name))
            return

        for callback in self._events[event_name]:
            LOG.debug("Firing callback for {}".format(event_name))
            callback(msg_obj[event_name])
