
def number_to_id(number):
    return number+'@c.us' if not '@c.us' in number else number

def send_text_message(driver, receiver, body):
    receiver = number_to_id(receiver)
    return driver.send_message_to_id(receiver, body)

def send_file_message(driver, path, receiver, body):
    return driver.send_media(path, receiver, body)

def get_number_status(driver, number):
    number = number_to_id(number)
    return driver.check_number_status(number)

def get_contacts_list(driver):
    return driver.get_contacts()