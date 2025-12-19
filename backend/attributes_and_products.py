# import csv
# import os

# # Создаем директорию для CSV файлов
# os.makedirs('csv_data', exist_ok=True)


# COFFEE_PRODUCTS = [1, 2, 3, 4, 5, 6, 7, 8]  # Эспрессо, Капучино, Латте, Флэт уайт, Айс латте, Фильтр-кофе, Бамбл-кофе, Тыквенный латте
# NON_COFFEE_PRODUCTS = [9, 10, 11, 12, 13, 14, 15, 16]  # Матча латте, Матча латте со льдом, Какао, Горячий шоколад, Апельсиновый фреш, Чай эрл грей, Клубничный матча-латте, Манго матча-латте

# attribute_types = [
#     {'attribute_name': 'milk'},
#     {'attribute_name': 'size'},
#     {'attribute_name': 'syrup'},
#     {'attribute_name': 'roast'},
# ]

# with open('csv_data/attribute_types.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['attribute_name'])
#     writer.writeheader()
#     writer.writerows(attribute_types)

# product_attribute_options = [
#     # Молоко (attribute_type_id = 1)
#     {'attribute_type_id': 1, 'value': 'Коровье молоко', 'extra_price': 0},
#     {'attribute_type_id': 1, 'value': 'Овсяное молоко', 'extra_price': 30},
#     {'attribute_type_id': 1, 'value': 'Миндальное молоко', 'extra_price': 30},
#     {'attribute_type_id': 1, 'value': 'Соевое молоко', 'extra_price': 30},
#     {'attribute_type_id': 1, 'value': 'Безлактозное молоко', 'extra_price': 20},
#     {'attribute_type_id': 1, 'value': 'Кокосовое молоко', 'extra_price': 30},
    
    
#     # Размер (attribute_type_id = 2)
#     {'attribute_type_id': 2, 'value': 'Маленький', 'extra_price': 0},
#     {'attribute_type_id': 2, 'value': 'Средний', 'extra_price': 40},
#     {'attribute_type_id': 2, 'value': 'Большой', 'extra_price': 60},
    
#     # Сироп (attribute_type_id = 3)
#     {'attribute_type_id': 3, 'value': 'Ванильный', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Карамельный', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Миндальный', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Шоколадный', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Кокосовый', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Кленовый', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Малиновый', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Лавандовый', 'extra_price': 30},
#     {'attribute_type_id': 3, 'value': 'Мятный', 'extra_price': 30},
    
#     # Обжарка (attribute_type_id = 4)
#     {'attribute_type_id': 4, 'value': 'Светлая', 'extra_price': 0},
#     {'attribute_type_id': 4, 'value': 'Средняя', 'extra_price': 0},
#     {'attribute_type_id': 4, 'value': 'Тёмная', 'extra_price': 0},
# ]

# with open('csv_data/product_attribute_options.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['attribute_type_id', 'value', 'extra_price'])
#     writer.writeheader()
#     writer.writerows(product_attribute_options)

# # 3. Связь продуктов с атрибутами (product_attributes)

# product_attributes = []

# MILK_OPTIONS = list(range(1, 7))      
# SIZE_OPTIONS = list(range(7, 10))     
# SYRUP_OPTIONS = list(range(10, 19)) 
# ROAST_OPTIONS = list(range(19, 22))

# for product_id in COFFEE_PRODUCTS:
#     # Молоко
#     for option_id in MILK_OPTIONS:
#         product_attributes.append({'product_id': product_id, 'option_id': option_id})
    
#     # Размер
#     for option_id in SIZE_OPTIONS:
#         product_attributes.append({'product_id': product_id, 'option_id': option_id})
    
#     # Сироп
#     for option_id in SYRUP_OPTIONS:
#         product_attributes.append({'product_id': product_id, 'option_id': option_id})
    
#     # Обжарка 
#     if product_id in [1, 2, 3, 4, 6]:
#         for option_id in ROAST_OPTIONS:
#             product_attributes.append({'product_id': product_id, 'option_id': option_id})

# for product_id in NON_COFFEE_PRODUCTS:
    
#     for option_id in SIZE_OPTIONS:
#         product_attributes.append({'product_id': product_id, 'option_id': option_id})
#     if product_id in [9, 10, 11, 12, 15, 16]:
#         for option_id in MILK_OPTIONS:
#             product_attributes.append({'product_id': product_id, 'option_id': option_id})
#     if product_id != 13 and product_id!=14:  #для чая и фреша не вставляем сиропы
#         for option_id in SYRUP_OPTIONS:
#             product_attributes.append({'product_id': product_id, 'option_id': option_id})

# with open('csv_data/product_attributes.csv', 'w', newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=['product_id', 'option_id'])
#     writer.writeheader()
#     writer.writerows(product_attributes)

# print("✓ CSV файлы созданы:")
# print(f"  - attribute_types.csv ({len(attribute_types)} записей)")
# print(f"  - product_attribute_options.csv ({len(product_attribute_options)} записей)")
# print(f"  - product_attributes.csv ({len(product_attributes)} записей)")
# print("\nРаспределение атрибутов:")
# print(f"  - Кофейные напитки (ID {COFFEE_PRODUCTS}): молоко, размер, сироп, обжарка")
# print(f"  - Некофейные напитки с молоком (ID 9,10,11,12,15,16): молоко, размер")
# print(f"  - Апельсиновый фреш (ID 13) и Чай эрл грей (ID 14): без атрибутов")

import csv
import os

# Создаем директорию для CSV файлов
os.makedirs('csv_data', exist_ok=True)

# Реальные ID продуктов из базы данных
COFFEE_PRODUCTS = [1, 2, 3, 4, 5, 6, 7, 8]
NON_COFFEE_PRODUCTS = [9, 10, 11, 12, 13, 14, 15, 16]

# 1. Типы атрибутов (attribute_types)
attribute_types = [
    {'attribute_name': 'milk'},
    {'attribute_name': 'size'},
    {'attribute_name': 'syrup'},
    {'attribute_name': 'roast'},
]

with open('csv_data/attribute_types.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['attribute_name'])
    writer.writeheader()
    writer.writerows(attribute_types)

# 2. Варианты атрибутов (product_attribute_options)
# Теперь используем названия атрибутов вместо ID
product_attribute_options = [
    # Молоко
    {'attribute_type': 'milk', 'value': 'Коровье молоко', 'extra_price': 0},
    {'attribute_type': 'milk', 'value': 'Овсяное молоко', 'extra_price': 30},
    {'attribute_type': 'milk', 'value': 'Миндальное молоко', 'extra_price': 30},
    {'attribute_type': 'milk', 'value': 'Соевое молоко', 'extra_price': 30},
    {'attribute_type': 'milk', 'value': 'Безлактозное молоко', 'extra_price': 20},
    {'attribute_type': 'milk', 'value': 'Кокосовое молоко', 'extra_price': 30},
    
    # Размер
    {'attribute_type': 'size', 'value': 'Маленький', 'extra_price': 0},
    {'attribute_type': 'size', 'value': 'Средний', 'extra_price': 40},
    {'attribute_type': 'size', 'value': 'Большой', 'extra_price': 60},
    
    # Сироп
    {'attribute_type': 'syrup', 'value': 'Ванильный', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Карамельный', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Миндальный', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Шоколадный', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Кокосовый', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Кленовый', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Малиновый', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Лавандовый', 'extra_price': 30},
    {'attribute_type': 'syrup', 'value': 'Мятный', 'extra_price': 30},
    
    # Обжарка
    {'attribute_type': 'roast', 'value': 'Светлая', 'extra_price': 0},
    {'attribute_type': 'roast', 'value': 'Средняя', 'extra_price': 0},
    {'attribute_type': 'roast', 'value': 'Тёмная', 'extra_price': 0},
]

with open('csv_data/product_attribute_options.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['attribute_type', 'value', 'extra_price'])
    writer.writeheader()
    writer.writerows(product_attribute_options)

# 3. Связь продуктов с атрибутами (product_attributes)
# Создаем словарь для быстрого поиска опций
options_dict = {}
option_counter = 1
for opt in product_attribute_options:
    key = (opt['attribute_type'], opt['value'])
    options_dict[key] = option_counter
    option_counter += 1

product_attributes = []

# Определяем списки опций по типам
milk_options = [(opt['attribute_type'], opt['value']) for opt in product_attribute_options if opt['attribute_type'] == 'milk']
size_options = [(opt['attribute_type'], opt['value']) for opt in product_attribute_options if opt['attribute_type'] == 'size']
syrup_options = [(opt['attribute_type'], opt['value']) for opt in product_attribute_options if opt['attribute_type'] == 'syrup']
roast_options = [(opt['attribute_type'], opt['value']) for opt in product_attribute_options if opt['attribute_type'] == 'roast']

# Кофейные напитки
for product_id in COFFEE_PRODUCTS:
    # Молоко
    for attr_type, value in milk_options:
        product_attributes.append({
            'product_id': product_id,
            'attribute_type': attr_type,
            'option_value': value
        })
    
    # Размер
    for attr_type, value in size_options:
        product_attributes.append({
            'product_id': product_id,
            'attribute_type': attr_type,
            'option_value': value
        })
    
    # Сироп
    for attr_type, value in syrup_options:
        product_attributes.append({
            'product_id': product_id,
            'attribute_type': attr_type,
            'option_value': value
        })
    
    # Обжарка (только для определенных напитков)
    if product_id in [1, 2, 3, 4, 6]:
        for attr_type, value in roast_options:
            product_attributes.append({
                'product_id': product_id,
                'attribute_type': attr_type,
                'option_value': value
            })

# Некофейные напитки
for product_id in NON_COFFEE_PRODUCTS:
    # Размер (для всех)
    for attr_type, value in size_options:
        product_attributes.append({
            'product_id': product_id,
            'attribute_type': attr_type,
            'option_value': value
        })
    
    # Молоко (для матча-латте и какао/шоколада)
    if product_id in [9, 10, 11, 12, 15, 16]:
        for attr_type, value in milk_options:
            product_attributes.append({
                'product_id': product_id,
                'attribute_type': attr_type,
                'option_value': value
            })
    
    # Сироп (для всех кроме чая)
    if product_id != 14:
        for attr_type, value in syrup_options:
            product_attributes.append({
                'product_id': product_id,
                'attribute_type': attr_type,
                'option_value': value
            })

with open('csv_data/product_attributes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'attribute_type', 'option_value'])
    writer.writeheader()
    writer.writerows(product_attributes)

print("✓ CSV файлы созданы:")
print(f"  - attribute_types.csv ({len(attribute_types)} записей)")
print(f"  - product_attribute_options.csv ({len(product_attribute_options)} записей)")
print(f"  - product_attributes.csv ({len(product_attributes)} записей)")
print("\nТеперь используются названия вместо ID:")
print("  - attribute_type вместо attribute_type_id")
print("  - option_value вместо option_id")