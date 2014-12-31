# -*- coding: utf-8 -*-
import collections
from gevent import Greenlet


class BaseMessagesSource(Greenlet):

    """Base class for messages source.
    For subclassing it do override `_run` method.
    """

    def __init__(self, on_message_callback, *args, **kwargs):
        """

        :param on_message_callback: function which expect one argument:
            def on_message_callback(raw_message):
                pass

        :param args:
        :param kwargs:
        :raise ValueError:
        """
        super(BaseMessagesSource, self).__init__(*args, **kwargs)
        if not isinstance(on_message_callback, collections.Callable):
            raise ValueError(
                'on_message_callback must be a function like '
                '`def x(raw_message): ...`'
            )

        # on_message_callback must be a function like `def x(raw_message)`
        self.on_message_callback = on_message_callback

    def _run(self):
        raise NotImplementedError(
            '{} is not implemented `_run` method'.format(
                self.__class__.__name__))
