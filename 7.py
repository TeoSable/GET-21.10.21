# Импортируем модули matplotlib для построения графиков, RPi.GPIO для работы с RaspberryPi и time для определения времени

import RPi.GPIO as GPIO
import matplotlib.pyplot as mpl
import time

# Записываем в переменные номера используемых портов, значения длины цифровых кодов и максимального напряжения 

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
bits = len(leds)
maxVoltage = 3.3
troykaModule = 17
comparator = 4

# Объявляем функцию преобразования десятичного числа в двоичный код

def dec2bin(dec):
    return [int(bit) for bit in bin(dec)[2:].zfill(bits)]

# Объявляем функцию преобразования десятичного числа в сигнал на DAC

def dec2dac(dec):
    GPIO.output(dac, dec2bin(dec))

# Объявляем функцию преобразования десятичного числа в сигнал на LEDs

def dec2leds(dec):
    GPIO.output(leds, dec2bin(dec))

# Объявляем функцию, считывающую значение напряжения на Тройка-модуле и преобразующую его в число от 0 до 255

def adc():
    val = 0
    for i in range(bits):
        dec2dac(2 ** (bits - i - 1) + val)
        time.sleep(0.001)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            val += 2 ** (bits - i - 1)
    return val 

# Задаём начальные настройки RPi.GPIO и подаём напряжение на схему

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troykaModule, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

try:
    # Начинаем измерения, фиксируем время начала
    startTime = time.time()
    value = 0
    n = 0
    data = []
    print("Начало зарядки конденсатора")

    # Пока конденсатор заряжается, считываем напряжение на нём и вносим значения в список
    while value < 252:
        value = adc()
        dec2leds(value)
        data.insert(n, value)
        n = n + 1
    
    # Перестаём подавать напряжение на схему
    GPIO.output(troykaModule, 0)
    print("Начало разрядки конденсатора")

    # Пока конденсатор разряжается, продолжаем считывать напряжение на нём и вносить значения в список
    while value > 3:
        value = adc()
        dec2leds(value)
        data.insert(n, value)
        n = n + 1

    # Завершаем эксперимент, рассчитываем длительность, период и частоту измерений
    endTime = time.time()
    print("Конец измерений")

    fullTime = endTime - startTime
    period = fullTime / n
    frequency = n / fullTime

    # Строим график изменения напряжения
    mpl.plot(data)
    mpl.show()

    # Преобразуем список значений в последовательность строк и экспортируем её в файл data.txt
    dataStr = [str(item) for item in data]

    with open("data.txt", "w") as file:
        file.write("\n".join(dataStr))

    # Экспортируем значение единицы напряжения и периода измерений в файл settings.txt

    voltageUnit = 1 / 256 * maxVoltage
    with open("settings.txt", "w") as file:
        file.write("Единица измерения напряжения - {} В \nПериод измерений - {} с".format(voltageUnit, period))

# В случае досрочного завершения программы с помощью клавиатуры выводим на экран сообщение об этом

except KeyboardInterrupt():
    print("The program has been interrupted")

# Проводим очистку GPIO и завершаем выполнение программы

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(leds, GPIO.LOW)
    GPIO.output(troykaModule, GPIO.LOW)
    GPIO.cleanup(dac)
    GPIO.cleanup(leds)
    GPIO.cleanup(comparator)
    GPIO.cleanup(troykaModule)
    print("GPIO cleanup complete.")