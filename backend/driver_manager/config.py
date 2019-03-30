from datetime import datetime

def get_number(id):
    from numbers_app.models import NumberSettings
    return NumberSettings.objects.get(number_id=id)

def current_time():
    return datetime.now().time()

def is_time_to_send(id):
    number = get_number(id)
    return number.send_schedule_from <= current_time() and number.send_schedule_to >= current_time()

def is_time_to_reboot(id):
    number = get_number(id)
    return number.auto_reboot == current_time()

def is_allowed_record(id):
    number = get_number(id)
    return number.record_inbox

def is_allowed_read(id):
    number = get_number(id)
    return number.auto_read

def get_max_delay(id):
    number = get_number(id)
    return number.max_delay

def get_delay_after(id):
    number = get_number(id)
    return number.delay_after