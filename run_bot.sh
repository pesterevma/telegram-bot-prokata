#!/bin/bash

# Путь к виртуальному окружению
VIRTUAL_ENV="/home/asus/manaraga_bot/test_bot2/venv/"

# Активация виртуального окружения
source "$VIRTUAL_ENV/bin/activate"

# Запуск вашего скрипта
python bot_telegram.py

# Ожидание ввода перед завершением
read -p "Press any key to exit..."