import time
import random
from pynput import keyboard, mouse

# Переменные для отслеживания состояния
last_released_key = None  # Последняя отпущенная клавиша ('a' или 'd')
hold_start_time = None  # Время начала удержания клавиши
release_time = None  # Время отпускания клавиши
release_timeout = 0.5  # Тайм-аут для ожидания нажатия мыши в секундах

# Генерация случайного времени удержания клавиши
def random_hold_time():
    return random.uniform(0.058, 0.08)  # от 58 до 80 мс

def press_opposite_key():
    global last_released_key

    if last_released_key == 'a':
        opposite_key = 'd'
    elif last_released_key == 'd':
        opposite_key = 'a'
    else:
        return  # Ничего не делаем, если нет последней отпущенной клавиши

    print(f"Simulating press of key '{opposite_key}'")
    
    # Эмулируем нажатие и удержание противоположной клавиши
    with keyboard.Controller() as controller:
        controller.press(opposite_key)
        time.sleep(random_hold_time())  # Удерживаем клавишу случайное время
        controller.release(opposite_key)
    
    last_released_key = None  # Сбрасываем состояние после нажатия

# Обработчик нажатий клавиш
def on_press_key(key):
    global hold_start_time

    try:
        if key.char == 'a' or key.char == 'd':
            hold_start_time = time.time()  # Запоминаем время начала удержания
    except AttributeError:
        pass

# Обработчик отпусканий клавиш
def on_release_key(key):
    global last_released_key, hold_start_time, release_time

    try:
        if key.char == 'a' or key.char == 'd':
            if hold_start_time is not None:
                hold_duration = (time.time() - hold_start_time) * 1000  # Длительность удержания в мс
                print(f"Key '{key.char}' was held for: {hold_duration:.2f} ms")
            last_released_key = key.char  # Запоминаем последнюю отпущенную клавишу
            hold_start_time = None  # Сбрасываем время удержания
            release_time = time.time()  # Запоминаем время отпускания
    except AttributeError:
        pass

# Обработчик нажатия мыши
def on_click(x, y, button, pressed):
    global release_time

    if button == mouse.Button.left and pressed:
        if release_time is not None:
            elapsed_time = time.time() - release_time
            if elapsed_time <= release_timeout:
                print("Left mouse button clicked within timeout")
                press_opposite_key()  # Нажимаем противоположную клавишу при клике левой кнопки мыши
            else:
                print("Left mouse button clicked after timeout")
        release_time = None  # Сбрасываем время отпускания

# Запуск глобального слушателя клавиатуры и мыши
with keyboard.Listener(on_press=on_press_key, on_release=on_release_key) as key_listener, \
     mouse.Listener(on_click=on_click) as mouse_listener:
    key_listener.join()
    mouse_listener.join()
