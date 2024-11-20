
""" Elasticsearch logging handler
"""

from logging import Logger


class LoggerService(Logger):

    def __define_log_level_sb(self, kwargs, login_level_sb):
        extra = kwargs.get("extra", {})
        if not extra:
            kwargs.update({"extra": extra})

        loggin_sb = extra.get("logging_level")
        if not loggin_sb:
            extra.update({"logging_level": login_level_sb})

    def exception(self, *args, **kwargs):
        self.__define_log_level_sb(kwargs, 'EXCEPTION')
        super(LoggerService, self).exception(*args, **kwargs)

    def health(self, *args, **kwargs):
        self.__define_log_level_sb(kwargs, 'HEALTH')
        super(LoggerService, self).info(*args, **kwargs)
