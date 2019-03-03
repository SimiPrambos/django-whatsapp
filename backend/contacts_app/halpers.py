from driver_manager.drivers import status_number

def number_checker(id, numbers):
    result = dict()
    for number in numbers:
        status = status_number(id, number)
        result[number] = status
    return result