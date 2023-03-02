#!/bin/bash

# Хочу проверить, все ли аргументы мы получили при вызове ./run.sh
if [[ $# -ne 3 ]]; then
    echo "Используемые аргументы: $0 <input_file> <output_file> <ratio>"
    exit 1
fi

# Сохраняем аргументы в переменные
input_file="$1"
output_file="$2"
ratio="$3"

python phase_vocoder.py "$input_file" "$output_file" "$ratio"

# Выведем что получилось у нас
echo "Файл $input_file обработан. Результат файл - $output_file"
