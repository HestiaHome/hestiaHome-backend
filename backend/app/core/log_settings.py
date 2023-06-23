import logging.config

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "std_format": {
            "format": "[{asctime} - {levelname} - {name}] {message}",
            "style": "{"
        }
    },
    "handlers": {
        "in_file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "std_format",
            "filename": "app_log.log"
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "std_format",
        }
    },
    "loggers": {
        "app_logger":{
            "level": "DEBUG",
            # "handlers": ["console", "in_file"],
            "handlers": ["console"],
            "filename": "log.log"
            # "propagate": False
        }
    },

    # "filters": {},
    # "root": {}, # '': {}
    # "incremental": True
}

logging.config.dictConfig(logger_config)

logger = logging.getLogger("app_logger")