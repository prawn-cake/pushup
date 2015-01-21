# -*- coding: utf-8 -*-
import unittest
from rocketws.registry import ChannelRegistry, SocketRegistry
from rocketws.tests import get_ws_client


if __name__ == '__main__':
    pass


class ChannelRegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = ChannelRegistry()

    def test_singleton(self):
        same_registry = ChannelRegistry()
        self.assertEqual(self.registry, same_registry)

    def test_subscribe(self):
        self.registry.flush_all()
        channel = 'john'
        client = get_ws_client()
        self.registry.subscribe(channel, client)

        self.assertEqual(len(self.registry.subscribers), 1)
        registered_client = self.registry.subscribers[0]
        self.assertEqual(registered_client.address, client.address)
        del client

        # Expected NoneType reference still not in sessions
        self.assertEqual(len(self.registry.subscribers), 0)
        self.assertEqual(
            len(self.registry.get_channel_subscribers(channel)), 0)

        client = get_ws_client()
        self.registry.subscribe(channel, client)
        # Expected NoneType reference will be removed and new one will be added
        self.assertEqual(len(self.registry.subscribers), 1)

    def test_subscribe_on_multiple_channels(self):
        self.registry.flush_all()
        client = get_ws_client()
        channel_1 = 'mark'
        channel_2 = 'kim'
        channel_3 = 'max'
        self.registry.subscribe(channel_1, client)
        self.registry.subscribe(channel_2, client)
        self.registry.subscribe(channel_3, client)
        self.assertEqual(len(self.registry.subscribers), 3)

    def test_subscribe_multiple_clients_for_one_channel(self):
        self.registry.flush_all()
        channel = 'chat'
        client_1 = get_ws_client()
        client_2 = get_ws_client()
        client_3 = get_ws_client()
        self.registry.subscribe(channel, client_1, client_2, client_3)

        # Expect {<channel>: [client_1, client_2, client_3]} storage
        self.assertEqual(len(self.registry.subscribers), 3)
        self.assertEqual(
            len(self.registry.get_channel_subscribers(channel)), 3)

    def test_notify_all(self):
        self.registry.flush_all()
        channel = 'chat'
        client_1 = get_ws_client()
        client_2 = get_ws_client()
        client_3 = get_ws_client()
        self.registry.subscribe(channel, client_1, client_2, client_3)
        self.registry.notify_all(data={'message': 'test'})

        for client in client_1, client_2, client_3:
            # mock for send method is injected in get_ws_client
            # message type will be added automatically
            client.ws.send.assert_called_once_with(
                '{"message": "test", "__type": "broadcast"}')


class SocketRegistryTestCase(unittest.TestCase):
    def setUp(self):
        self.registry = SocketRegistry()

    def test_register(self):
        self.registry.flush()
        client = get_ws_client()
        self.registry.register(client)
        self.assertEqual(len(self.registry.clients), 1, self.registry.clients)

    def test_unregister(self):
        self.registry.flush()
        client = get_ws_client()
        self.registry.register(client)
        self.registry.unregister(client)
        self.assertEqual(len(self.registry.clients), 0)

    def test_get_client(self):
        self.registry.flush()
        client = get_ws_client()
        self.registry.register(client)
        self.registry.register(client)
        _client = self.registry.get_client(client.address)
        self.assertEqual(client, _client)