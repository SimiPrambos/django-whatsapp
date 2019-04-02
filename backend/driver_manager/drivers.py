import os, shutil, threading, time, random
from .webwhatsapi import WhatsAPIDriver, WhatsAPIDriverStatus
from selenium.common.exceptions import WebDriverException, TimeoutException
from .handlers import RepeatedTimer, HandleReceivedMessage, HandleSendMessage
from django.conf import settings
from .config import (
    is_time_to_reboot,
    is_time_to_send,
    is_allowed_record,
    is_allowed_read,
    get_max_delay,
    get_delay_after
)
from messages_app.models import WhatsappChatMessages, WhatsappMediaMessages

drivers = dict()
timers = dict()
semaphores = dict()
messages = dict()


def init_driver(id):
    profile_path = settings.CHROME_CACHE_PATH + str(id)
    print(profile_path)
    if not os.path.exists(profile_path):
        print("sip")
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
    timers[id] = RepeatedTimer(5, background_task, id)

def background_task(id):
    if (id not in drivers or not drivers[id]):
        timers[id].stop()
        return
    
    if not drivers[id].is_logged_in():
        return

    if not acquire_semaphore(id, True):
        return

    if is_time_to_reboot(id):
        reboot_instance()
        return
    
    try:
        release_semaphore(id)
        # if drivers[id].is_logged_in():
        if is_time_to_send(id):
            outbound_message_background(id)
        if is_allowed_record(id):
            incoming_message_background(id)
    except Exception:
        # drivers.pop(id)
        pass
    finally:
        release_semaphore(id)

def incoming_message_background(id):
    messages = drivers[id].get_unread(use_unread_count=True)
    if messages:
        if is_allowed_read(id):
            for message in messages:
                message.chat.send_seen()
        HandleReceivedMessage(id, messages).start()

def outbound_message_background(id):
    chats = WhatsappChatMessages.objects.filter(
        number_id=id, message_type='OUT',
        message_status='P', send_retry__lt=3,
        on_progress=False
    )
    medias = WhatsappMediaMessages.objects.filter(
        number_id=id, message_type='OUT',
        message_status='P', send_retry__lt=3,
        on_progress=False
    )
    max_delay = get_max_delay(id)
    max_delay = 2 if max_delay <= 2 else max_delay
    delay_after = get_delay_after(id)
    
    if chats:
        for index, chat in enumerate(chats, start=1):
            chat.on_progress = True
            chat.save()
        for chat in chats:
            messages[id] += 1
            if messages[id] > 0 and messages[id] % delay_after == 0:
                time.sleep(120)
            time.sleep(random.randint(max_delay//2, max_delay))
            send = HandleSendMessage(id=id, instance=chat)
            send.start()
            send.join()

    if medias:
        for index, media in enumerate(medias, start=1):
            media.on_progress = True
            media.save()
        for media in medias:
            messages[id] += 1
            if messages[id] > 0 and messages[id] % delay_after == 0:
                time.sleep(120)
            time.sleep(random.randint(max_delay//2, max_delay))
            send = HandleSendMessage(id=id, instance=media, media=True)
            send.start()
            send.join()
        
def delete_client(id, remove_cache):
    if id in drivers:
        drivers.pop(id).quit()

    if remove_cache:
        path = settings.CHROME_CACHE_PATH + str(id)
        if os.path.exists(path):
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
def get_instance(id):
    return drivers[id] if id in drivers and drivers[id] else None

def start_instance(id):
    instance = init_client(id)
    # try:
    #     instance.wait_for_login(timeout=5)
    # except TimeoutException:
    #     pass
    time.sleep(5)
    messages[id] = 0
    init_timer(id)
    return instance

def stop_instance(id):
    status = False
    if id in drivers:
        drivers.pop(id).quit()
        try:
            timers[id].stop()
            timers[id] = None
            release_semaphore(id)
            semaphores[id] = None
            status = True
        except:
            pass
    else:
        status = True
    return status

def reboot_instance(id):
    status = False
    try:
        stop_instance(id)
        start_instance(id)
        status = True
    except:
        pass
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