""" Elasticsearch logging handler
"""
import json
import logging
from datetime import date
from threading import Lock, Timer

import urllib3

from src.internal_services.app_request import RequestsApp

urllib3.disable_warnings()


class HandlerService(logging.Handler):
    """ Elasticsearch log handler

    Allows to log to elasticsearch into json format.
    All LogRecord fields are serialised and inserted
    """

    def __init__(self,
                 host='http:://localhost:9200',
                 use_ssl=False,
                 buffer_size=1000,
                 flush_frequency_in_sec=1,
                 es_index_name='python_logger',
                 es_doc_type='line'):

        logging.Handler.__init__(self)

        self.host = host
        self.use_ssl = use_ssl
        self.buffer_size = buffer_size
        self.flush_frequency_in_sec = flush_frequency_in_sec
        self.es_index_name = es_index_name
        self.es_doc_type = es_doc_type
        self._buffer = []
        self._buffer_lock = Lock()
        self._timer = None

    @property
    def __request(self):
        return RequestsApp()

    def __schedule_flush(self):
        if self._timer is None:
            self._timer = Timer(self.flush_frequency_in_sec, self.flush)
            self._timer.setDaemon(True)
            self._timer.start()

    def __send_elastic(self, buffer_log):
        index = '{index}-{date}'.format(index=self.es_index_name, date=date.today().strftime("%Y.%m.%d"))
        url = "{host}/{_index}/{_type}/_bulk".format(host=self.host, _index=index, _type=self.es_doc_type)
        body = '\n'.join(map(lambda line: '{"index":{}}' + '\n' + json.dumps(line), buffer_log)) + '\n'
        self.__request.post(url, data=body, verify=self.use_ssl, headers={'content-type': 'application/json'})

    def __check_timer(self):
        if self._timer is not None and self._timer.is_alive():
            self._timer.cancel()
        self._timer = None

    def flush(self):
        """ Flushes the buffer into ES
        :return: None
        """
        self.__check_timer()
        if self._buffer:
            try:
                with self._buffer_lock:
                    logs_buffer = self._buffer
                    self._buffer = []
                self.__send_elastic(logs_buffer)
            except Exception as exception:
                self.handleError(exception)

    def emit(self, record):
        """ Emit overrides the abstract logging.Handler logRecord emit method

        Format and records the log

        :param record: A class of type ```logging.LogRecord```
        :return: None
        """
        rec = self.format(record)
        with self._buffer_lock:
            self._buffer.append(rec)

        if len(self._buffer) >= self.buffer_size:
            self.flush()
            return
        self.__schedule_flush()
