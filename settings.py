ASYNC = {
    'timeout': 0.1,  # timeout in seconds
    'retries': 3,
    'semaphore': 1000  # max number of concurrent tasks
}

THREAD = {
    'workers': 4,  # number of threads
    'timeout': 0.1,  # timeout in seconds
    'retries': 2
}

PROXY = {
    'quorum': 10,
    'source': 'https://hidemyna.me/en/proxy-list/?maxtime=1000&type=h#list'
}

UNREACHED_URLS_PATH = 'unreached.txt'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'WARN',
            'formatter': 'brief',
            'stream': 'ext://sys.stderr',
        },
        'async_file_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/async_crawler.log',
            'formatter': 'full',
            # You can use the when to specify the type of interval. Rotating happens based on the product of WHEN
            # and INTERVAL. (Only for 'file' handler). Allowed values:
            # 'S' - Seconds
            # 'M' - Minutes
            # 'H' - Hours
            # 'D' - Days
            # 'W0', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6' - Weekday (0=Monday)
            # 'midnight' - Roll over at midnight
            'when': 'D',
            # After how many WHEN units should log be rotated.
            'interval': 2,
            # Number of rotated logs.
            'backupCount': 2,
        },
        'thread_file_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/thread_crawler.log',
            'formatter': 'full',
            # You can use the when to specify the type of interval. Rotating happens based on the product of WHEN
            # and INTERVAL. (Only for 'file' handler). Allowed values:
            # 'S' - Seconds
            # 'M' - Minutes
            # 'H' - Hours
            # 'D' - Days
            # 'W0', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6' - Weekday (0=Monday)
            # 'midnight' - Roll over at midnight
            'when': 'D',
            # After how many WHEN units should log be rotated.
            'interval': 2,
            # Number of rotated logs.
            'backupCount': 2,
        },
        'proxies_file_log': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/proxies.log',
            'formatter': 'full',
            # You can use the when to specify the type of interval. Rotating happens based on the product of WHEN
            # and INTERVAL. (Only for 'file' handler). Allowed values:
            # 'S' - Seconds
            # 'M' - Minutes
            # 'H' - Hours
            # 'D' - Days
            # 'W0', 'W1', 'W2', 'W3', 'W4', 'W5', 'W6' - Weekday (0=Monday)
            # 'midnight' - Roll over at midnight
            'when': 'D',
            # After how many WHEN units should log be rotated.
            'interval': 2,
            # Number of rotated logs.
            'backupCount': 2,
        },
    },
    'formatters': {
        'brief': {
            'format': '[%(asctime)s] %(message)s',
        },
        'full': {
            'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'debug': {
            'format': '%(asctime)s %(levelname)s [%(threadName)s:%(name)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'loggers': {
        'async_crawler': {
            'handlers': ['async_file_log', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'thread_crawler': {
            'handlers': ['thread_file_log', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'proxies': {
            'handlers': ['proxies_file_log', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

PROXY_IPS = ['37.110.74.225:8181', '85.26.146.169:80', '195.13.199.219:53796']

DEFAULT_FITNESS = .1

MINIMAL_FITNESS = .01
MAXIMAL_FITNESS = 1
