import os, shutil, threading
from .webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from selenium.common.exceptions import WebDriverException
from .handlers import RepeatedTimer
from django.conf import settings
from .notifier import HandleReceivedMessage

drivers = dict()
timers = dict()
semaphores = dict()


def init_driver(id):
    profile_path = settings.CHROME_CACHE_PATH + str(id)
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    chrome_options = [
        'window-size=' + settings.CHROME_WINDOW_SIZE,
        '--user-agent=' + settings.USER_AGENT
    ]

    if settings.CHROME_IS_HEADLESS:
        chrome_options.append('--headless')
    if settings.CHROME_DISABLE_SANDBOX:
        chrome_options.append('--no-sandbox')
    if settings.CHROME_DISABLE_GPU:
        chrome_options.append('--disable-gpu')
    
    d = WhatsAPIDriver(
        username=id, 
        profile=profile_path, 
        client='chrome', 
        chrome_options=chrome_options
    )
    return d


def init_client(id):
    if id not in drivers:
        drivers[id] = init_driver(id)
    return drivers[id]


def init_timer(id):
    if id in timers and timers[id]:
        timers[id].start()
        return
    timers[id] = RepeatedTimer(10, check_status, id)

def check_status(id):
    if (id not in drivers or not drivers[id]):
        timers[id].stop()
        return
    
    if not acquire_semaphore(id, True):
        return
    try:
        res = drivers[id].get_unread(use_unread_count=True)
        for message_group in res:
            message_group.chat.send_seen()
        release_semaphore(id)
        if res:
            HandleReceivedMessage(id, res).start()
    except Exception:
        drivers.pop(id)
    finally:
        release_semaphore(id)


def delete_client(id, remove_cache):
    if id in drivers:
        drivers.pop(id).quit()

    if remove_cache:
        path = settings.CHROME_CACHE_PATH + str(id)
        shutil.rmtree(path)


def acquire_semaphore(id, cancel_if_locked=False):
    if not id:
        return False

    if id not in semaphores or semaphores[id] is None:
        semaphores[id] = threading.Semaphore()

    timeout = 10
    if cancel_if_locked:
        timeout = 0

    val = semaphores[id].acquire(blocking=True, timeout=timeout)

    return val

def release_semaphore(id):
    if not id:
        return False

    if id in semaphores and not semaphores[id] is None:
        semaphores[id].release()

###########################################
def start_instance(id):
    instance = init_client(id)
    init_timer(id)
    return instance

def stop_instance(id):
    status = False
    if id in drivers:
        try:
            drivers.pop(id).quit()
            status = True
        except:
            pass
    else:
        status = True
    return status

def status_instance(id):
    is_running = False
    is_logged_in = False
    if id in drivers and drivers[id]:
        is_running = True
    if is_running:
        is_logged_in = drivers[id].is_logged_in()
    return {"is_running":is_running, "is_logged_in":is_logged_in}

def status_number(id, number):
    status = drivers[id].check_number_status(number).status
    return True if status is 200 else False

def send_message(id, to, content):
    status = False
    try:
        status = drivers[id].send_message_to_id(to, content)
    except:
        pass
    return 'D' if status else 'F'

def send_media(id, to, caption, filepath):
    status = False
    try:
        status = drivers[id].send_media(filepath, to, caption)
    except:
        pass
    return 'D' if status else 'F'