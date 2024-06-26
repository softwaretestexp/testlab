import requests
import time
from .logger import getLogger
import sys
import typing

# Globals
# single retry count, how many times will post retry
POST_RETRIES = 5
# time out in seconds each time
POST_TIMEOUT = 60 * 5

# how many times will post retry on throttle limit
THROTTLE_RETRIES = 500
# wait few seconds each time on throttle retry
THROTTLE_TIMEWAIT = 6

def download(url: str, fp: typing.IO, **kwargs) -> typing.IO:
    """Wrapper requests.post call"""
    logger = getLogger("REQUEST")
    logger.debug(f"URL: {url}")
    kwargs["timeout"] = 20
    try:
        for j in range(THROTTLE_RETRIES):
            for i in range(POST_RETRIES):
                try:
                    # NOTE the stream=True parameter below
                    with requests.get(url, stream=True, **kwargs) as resp:
                        if resp.status_code == 401:
                            raise ValueError("REST ERROR: Invalid authorization/token")
                        if resp.status_code == 429 or resp.status_code == 502:
                            # throttle limit error
                            time.sleep(THROTTLE_TIMEWAIT)
                            continue
                        resp.raise_for_status()
                        total_size = resp.headers.get("Content-Length", -1)
                        for chunk in resp.iter_content(chunk_size=32 * 1024, decode_unicode=False):
                            if chunk:
                                fp.write(chunk)
                        act_filesize = fp.tell()
                        if int(act_filesize) != int(total_size):
                            raise ValueError(
                                f"Download incomplete({act_filesize}/{total_size}) due to http connection close!"
                            )
                    return fp
                except (
                    requests.ConnectionError,
                    requests.Timeout,
                    requests.exceptions.ChunkedEncodingError,
                ) as e:
                    if i == POST_RETRIES - 1:
                        raise requests.Timeout(e)
                    else:
                        if fp.seekable():
                            fp.seek(0)
                            fp.truncate()
                        time.sleep(1)
                        continue
    except requests.exceptions.RequestException as e:
        logger.critical(e)
        raise e
    return fp


def get(url: str, params=None, **kwargs) -> requests.Response:
    """Wrapper requests.post call"""
    logger = getLogger("REQUEST")
    logger.debug(f"URL: {url}")
    kwargs["timeout"] = POST_TIMEOUT
    try:
        for j in range(THROTTLE_RETRIES):
            for i in range(POST_RETRIES):
                try:
                    resp = requests.get(url, params, **kwargs)
                    break
                except (requests.ConnectionError, requests.Timeout) as e:
                    if i == POST_RETRIES - 1:
                        raise e
                    else:
                        continue
            if resp.status_code == 401:
                raise ValueError("REST ERROR: Invalid authorization/token")
            if resp.status_code == 429 or resp.status_code == 502:
                # throttle limit error
                time.sleep(THROTTLE_TIMEWAIT)
                continue
            if resp.status_code < 200 or resp.status_code >= 300:
                raise ValueError(f"REST ERROR: Failed code={resp.status_code}, msg={resp.text}")
            # Get data dictionary from JSON Data
            data = resp
            break
    except requests.exceptions.RequestException as e:
        logger.critical(e)
        resp = None
        data = None
        raise e
    return data


def post(url: str, data: str = None, json=None, **kwargs) -> requests.Response:
    """Wrapper requests.post call"""
    logger = getLogger("REQUEST")
    logger.debug(f"URL: {url}")
    kwargs["timeout"] = POST_TIMEOUT
    try:
        for j in range(THROTTLE_RETRIES):
            for i in range(POST_RETRIES):
                try:
                    resp = requests.post(url, data, json, **kwargs)
                    break
                except (requests.ConnectionError, requests.Timeout) as e:
                    if i == POST_RETRIES - 1:
                        raise e
                    else:
                        continue
            if resp.status_code == 401:
                raise ValueError("REST ERROR: Invalid authorization/token")
            if resp.status_code == 429:
                # throttle limit error
                time.sleep(THROTTLE_TIMEWAIT)
                continue
            if resp.status_code < 200 or resp.status_code >= 300:
                logger.warning(f"REST ERROR: Failed code={resp.status_code}, msg={resp.text}")
            break
    except requests.exceptions.RequestException as e:
        logger.critical(e)
        resp = None
        raise e
    return resp


def put(url: str, data: str = None, **kwargs) -> requests.Response:
    """Wrapper requests.put call"""
    logger = getLogger("REQUEST")
    logger.debug(f"URL: {url}")
    kwargs["timeout"] = POST_TIMEOUT
    try:
        for j in range(THROTTLE_RETRIES):
            for i in range(POST_RETRIES):
                try:
                    resp = requests.put(url, data, **kwargs)
                    break
                except (requests.ConnectionError, requests.Timeout) as e:
                    if i == POST_RETRIES - 1:
                        raise e
                    else:
                        continue
            if resp.status_code == 401:
                raise ValueError("REST ERROR: Invalid authorization/token")
            if resp.status_code == 429:
                # throttle limit error
                time.sleep(THROTTLE_TIMEWAIT)
                continue
            if resp.status_code < 200 or resp.status_code >= 300:
                logger.warning(f"REST ERROR: Failed code={resp.status_code}, msg={resp.text}")
            break
    except requests.exceptions.RequestException as e:
        logger.critical(e)
        resp = None
        raise e
    return resp


def delete(url: str, **kwargs) -> requests.Response:
    """Wrapper requests.put call"""
    logger = getLogger("REQUEST")
    logger.debug(f"URL: {url}")
    kwargs["timeout"] = POST_TIMEOUT
    try:
        for j in range(THROTTLE_RETRIES):
            for i in range(POST_RETRIES):
                try:
                    resp = requests.delete(url, **kwargs)
                    break
                except (requests.ConnectionError, requests.Timeout) as e:
                    if i == POST_RETRIES - 1:
                        raise e
                    else:
                        continue
            if resp.status_code == 401:
                raise ValueError("REST ERROR: Invalid authorization/token")
            if resp.status_code == 429:
                # throttle limit error
                time.sleep(THROTTLE_TIMEWAIT)
                continue
            if resp.status_code < 200 or resp.status_code >= 300:
                raise ValueError(f"REST ERROR: Failed code={resp.status_code}, msg={resp.text}")
            break
    except requests.exceptions.RequestException as e:
        logger.critical(e)
        resp = None
        raise e
    return resp
