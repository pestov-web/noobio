import threading
import time
import random
from pynput import keyboard

# Переменные для отслеживания состояния клавиш и блокировки
a_pressed = False
d_pressed = False
shift_pressed = False
listener_enabled = True  # Флаг для управления работой слушателя

# Создаем контроллер клавиатуры один раз для повторного использования
controller = keyboard.Controller()

# Функция для эмуляции нажатия и удержания противоположной клавиши с рандомной задержкой
def press_key(key):
    global listener_enabled
    listener_enabled = False  # Отключаем слушатель на время симуляции
    
    # Рандомная задержка перед отпусканием клавиши в интервале от 0.3 до 0.7 секунд
    hold_time = random.uniform(0.3, 0.7)
    
    controller.press(key)
    time.sleep(hold_time)  # Удерживаем клавишу на рандомное время
    controller.release(key)
    
    # Дополнительная рандомная задержка перед включением слушателя
    time.sleep(random.uniform(0.3, 0.7))
    listener_enabled = True  # Включаем слушатель обратно

# Функция для запуска таймера и эмуляции нажатия противоположной клавиши с рандомным таймаутом
def start_timer_and_press_opposite(key):
    global shift_pressed
    if shift_pressed:
        return  # Если Shift зажат, не выполняем действия

    # Рандомный тайм-аут в диапазоне от 0.2 до 0.6 секунд
    random_timeout = random.uniform(0.2, 0.6)
    
    # Ждем случайный промежуток времени, а затем эмулируем нажатие
    threading.Timer(random_timeout, lambda: press_key(key)).start()

# Функция обработки нажатий клавиш
def on_press(key):
    global a_pressed, d_pressed, shift_pressed, listener_enabled
    if not listener_enabled:  # Если слушатель отключен, игнорируем события
        return

    try:
        if key.char == 'a':
            a_pressed = True
        elif key.char == 'd':
            d_pressed = True
    except AttributeError:
        # Обрабатываем специальные клавиши, например Shift
        if key == keyboard.Key.shift:
            shift_pressed = True

# Функция обработки отпускания клавиш
def on_release(key):
    global a_pressed, d_pressed, shift_pressed, listener_enabled
    if not listener_enabled:  # Если слушатель отключен, игнорируем события
        return

    try:
        if key.char == 'a':
            a_pressed = False
            if not shift_pressed:  # Если Shift не зажат
                start_timer_and_press_opposite('d')  # Запускаем таймер для D
        elif key.char == 'd':
            d_pressed = False
            if not shift_pressed:  # Если Shift не зажат
                start_timer_and_press_opposite('a')  # Запускаем таймер для A
    except AttributeError:
        # Обрабатываем специальные клавиши
        if key == keyboard.Key.shift:
            shift_pressed = False

# Запуск глобального слушателя клавиатуры
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
