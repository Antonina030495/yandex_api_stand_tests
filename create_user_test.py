# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request

# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data
# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1
    print(str_user)

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
test_create_user_2_letter_in_first_name_get_success_response()

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")
test_create_user_15_letter_in_first_name_get_success_response()

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    print(user_response.json())

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")
test_create_user_1_letter_in_first_name_get_error_response()

def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")
test_create_user_16_letter_in_first_name_get_error_response()

def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")
test_create_user_english_letter_in_first_name_get_success_response()

def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Василий")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Ва силий")

def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("Ва?силий")
test_create_user_has_special_symbol_in_first_name_get_error_response()

def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("Ва4силий")
test_create_user_has_number_in_first_name_get_error_response()

def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"
    print(user_response.json())

# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)
test_create_user_no_first_name_get_error_response()

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)
test_create_user_empty_first_name_get_error_response()

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    user_response = sender_stand_request.post_new_user(user_body)
    print(user_response.json())
    assert user_response.status_code == 400
test_create_user_number_type_first_name_get_error_response()

