import threading
import time
from pynput import keyboard

# Переменные для отслеживания состояния клавиш и блокировки
a_pressed = False
d_pressed = False
shift_pressed = False
timeout = 5  # Таймаут в секундах (уменьшен до 5 секунд)
hold_time = 0.5  # Время удержания клавиши в секундах для "человеческого" эффекта
is_simulating = False  # Флаг для блокировки обработки эмулируемых нажатий

# Создаем контроллер клавиатуры один раз для повторного использования
controller = keyboard.Controller()

# Функция для эмуляции нажатия и удержания противоположной клавиши
def press_key(key):
    global is_simulating
    is_simulating = True  # Включаем флаг симуляции
    controller.press(key)
    time.sleep(hold_time)  # Удерживаем клавишу на заданное время
    controller.release(key)
    is_simulating = False  # Отключаем флаг симуляции

# Функция для запуска таймера и эмуляции нажатия противоположной клавиши
def start_timer_and_press_opposite(key):
    global shift_pressed
    if shift_pressed:
        return  # Если Shift зажат, не выполняем действия

    # Ждем 5 секунд, а затем эмулируем нажатие
    threading.Timer(timeout, lambda: press_key(key)).start()

# Функция обработки нажатий клавиш
def on_press(key):
    global a_pressed, d_pressed, shift_pressed, is_simulating
    if is_simulating:  # Если в данный момент идет симуляция, игнорируем события
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
    global a_pressed, d_pressed, shift_pressed, is_simulating
    if is_simulating:  # Если в данный момент идет симуляция, игнорируем события
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
