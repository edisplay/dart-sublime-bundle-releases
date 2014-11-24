# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

"""Responses from the analyzer.
"""

import sublime

import queue

from Dart.sublime_plugin_lib import PluginLogger
from Dart.lib.analyzer.api.notifications import ErrorsNotification


_logger = PluginLogger(__name__)


class ResponseMaker(object):
    '''Transforms raw notification and responses into `ServerResponse`s.
    '''

    def __init__(self, source):
        self.source = source

    def make(self):
        '''Makes `ServerResponse`s forever.

        Note: This will potentially saturate a process, so make sure to pause
        if the yielded value is `None`.
        '''
        while True:
            try:
                data = self.source.get()
            except queue.Empty:
                # unreachable?
                _logger.error('unexpected empty queue in ResponseMaker')
                yield
                continue

            if data.get('_internal') is not None:
                yield data
                break

            r = response_classifier(data)

            yield r


def is_result_id_response(data):
    return data.get('result', {}).get('id')


def is_result_response(data):
    return data.get('event') == 'search.results'


def is_errors_response(data):
    return data.get('event') == 'analysis.errors'


def response_classifier(data):
    # XXX: replace here XXX
    if is_errors_response(data):
        return ErrorsNotification(data)
    return None
