


def calculate_nights(check_in, check_out):
    return (check_out - check_in).days


def calculate_price(room_price, nights):
    return room_price * nights