from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

#  1 test
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

#  2 test
def test_get_all_pets_with_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

#  3 test
def test_add_new_pet_with_valid_data(name='Барбскин', animal_type='двртерьер',
                                     age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#  4 test
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

#  5 test
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#  6 test
def test_add_pet_without_photo(name='Каша', animal_type='собака', age='8'):
    """ Проверяем возможность добавления питомца без фото"""

    #  Получаем ключ auth_key и сохраняем в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  заводим питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    #  сверяем полученный результат с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

#  7 test
def test_add_photo_pet_by_id(pet_photo='images/P1040103.jpg'):
    """ Проверяем возможность добавления фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Получаем ключ auth_key и сохраняем в auth_key, а так же получаем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo_by_pet_id(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#  8 test
def test_get_api_key_with_invalid_user_email(email='pet@yandex.ru', password=valid_password):
    """ Проверяем что запрос api ключа с неправильным email и правильным паролем
    ответ сервера должен быть 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

#  8 test
def test_get_api_key_with_invalid_user_password(email=valid_email, password='12345'):
    """ Проверяем что запрос api ключа с неправильным паролем и правильным email
    ответ сервера должен быть 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

#  9 test
def test_add_photo_bmp_pet_by_id(pet_photo='images/Goluboglaz.bmp'):
    """ Проверяем возможность добавления фото в формате BMP питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Получаем ключ auth_key и сохраняем в auth_key, а так же получаем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo_by_pet_id(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#  10 test
def test_add_new_pet_with_empty_name(name='', animal_type='двртерьер',
                                     age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с пустым именем"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''

#  11 test
def test_add_new_pet_with_empty_animal_type(name='Viksi', animal_type='',
                                     age='5', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с пустым animal_type"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['animal_type'] == ''

#  12 test
def test_add_new_pet_with_empty_age(name='Кроха', animal_type='',
                                     age='', pet_photo='images/Goluboglaz.bmp'):
    """Проверяем что можно добавить питомца с пустым animal_type и age"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == ''

#  13 test
def test_add_new_pet_with_empty_all(name='', animal_type='',
                                     age='', pet_photo='images/Goluboglaz.bmp'):
    """Проверяем что можно добавить питомца со всеми пустым полями но с фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''
    assert result['animal_type'] == ''
    assert result['age'] == ''

#  14 test
def test_add_pet_without_photo_with_all_empty(name='', animal_type='', age=''):
    """ Проверяем возможность добавления питомца без всех данных"""

    #  Получаем ключ auth_key и сохраняем в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #  заводим питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    #  сверяем полученный результат с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''
    assert result['animal_type'] == ''
    assert result['age'] == ''
    print('This addition is not allowed.')

#  15 test
def test_add_new_pet_with_invalid_age(name='Кроха', animal_type='',
                                     age='fshk', pet_photo='images/Goluboglaz.bmp'):
    """Проверяем что нельзя добавлять питомца с неверным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

#  16 test
def test_add_photo_pet_by_id_with_photo(pet_photo='images/P1040103.jpg'):
    """ Проверяем возможность добавления фото питомца, питомцу у которого уже есть фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    #  Получаем ключ auth_key и сохраняем в auth_key, а так же получаем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем добавить фото
    if len(my_pets['pets']) > 0:
        """ два раза вызываем функцию что бы убедиться что у питомца точно будет фото"""
        status, result = pf.add_pet_photo_by_pet_id(auth_key, my_pets['pets'][0]['id'], pet_photo)
        status, result = pf.add_pet_photo_by_pet_id(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
