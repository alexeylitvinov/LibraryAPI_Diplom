def generate_library_card_number(user_id):
    """ Генерация номера библиотечной карточки """
    card_number = str(user_id).zfill(6)
    return card_number
