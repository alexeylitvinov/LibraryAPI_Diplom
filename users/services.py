def generate_library_card_number(user_id):
    card_number = str(user_id).zfill(6)
    return card_number
