from typing import Any


def settings() -> dict[str, Any]:
    setup = {
        'CONCURRENT_REQUESTS': 4,
        'CONCURRENT_REQUESTS_PER_IP': 4,
        'DOWNLOAD_DELAY': 0.114,
        'FEED_EXPORT_ENCODING': "utf-8",
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'REDIRECT_ENABLED': False,
        'RETRY_ENABLED': False,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        # 'RETRY_TIMES': 8,
    }
    return setup
