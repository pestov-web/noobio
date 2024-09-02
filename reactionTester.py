import time
from pynput import keyboard

# Переменные для отслеживания времени
time_between_a_and_d = None  # Время между отпусканием A и нажатием D
time_between_d_and_a = None  # Время между отпусканием D и нажатием A
hold_start_time_a = None  # Время начала удержания клавиши A
hold_start_time_d = None  # Время начала удержания клавиши D

def on_press(key):
    global time_between_a_and_d, time_between_d_and_a
    global hold_start_time_a, hold_start_time_d

    try:
        if key.char == 'a':  # Если нажата клавиша 'A'
            hold_start_time_a = time.time()  # Запоминаем время начала удержания A
            if time_between_d_and_a is not None:
                elapsed_time = (time.time() - time_between_d_and_a) * 1000  # Время между отпусканием D и нажатием A
                print(f"Time between releasing D and pressing A: {elapsed_time:.2f} ms")
                time_between_d_and_a = None  # Сбросим время
        elif key.char == 'd':  # Если нажата клавиша 'D'
            hold_start_time_d = time.time()  # Запоминаем время начала удержания D
            if time_between_a_and_d is not None:
                elapsed_time = (time.time() - time_between_a_and_d) * 1000  # Время между отпусканием A и нажатием D
                print(f"Time between releasing A and pressing D: {elapsed_time:.2f} ms")
                time_between_a_and_d = None  # Сбросим время
    except AttributeError:
        pass

def on_release(key):
    global time_between_a_and_d, time_between_d_and_a
    global hold_start_time_a, hold_start_time_d

    try:
        if key.char == 'a':  # Если отпустили клавишу 'A'
            if hold_start_time_a is not None:
                hold_duration = (time.time() - hold_start_time_a) * 1000  # Длительность удержания A в мс
                print(f"Key A was held for: {hold_duration:.2f} ms")
            time_between_a_and_d = time.time()  # Запоминаем время отпускания A
            hold_start_time_a = None  # Сбрасываем время удержания A
        elif key.char == 'd':  # Если отпустили клавишу 'D'
            if hold_start_time_d is not None:
                hold_duration = (time.time() - hold_start_time_d) * 1000  # Длительность удержания D в мс
                print(f"Key D was held for: {hold_duration:.2f} ms")
            time_between_d_and_a = time.time()  # Запоминаем время отпускания D
            hold_start_time_d = None  # Сбрасываем время удержания D
    except AttributeError:
        pass

# Запуск глобального слушателя клавиатуры
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
