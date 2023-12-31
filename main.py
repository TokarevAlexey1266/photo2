from icrawler.builtin import GoogleImageCrawler
import pandas as pd
import os
from ImageParser import YandexImage
import wget

# Укажите путь к XLS файлу, где содержится список ключевых слов
xls_file_path = '/home/superiorkilljoy/Projects/image_parser/names.xlsx'

# Загрузите данные из XLS файла
df = pd.read_excel(xls_file_path)

# Задайте путь для сохранения изображений
base_storage_path = '/home/superiorkilljoy/Projects/image_parser/images'

parser = YandexImage()
count = 0

# Создадим отдельную папку для каждого имени
for index, row in df.iterrows():
    name = row['Keyword']  # Предполагается, что в XLS файле есть столбец с названием "Keyword"
    quantity = 1000  # Количество загружаемых фотографий
    storage_path = os.path.join(base_storage_path, name)  # Путь для сохранения фотографий для текущего имени

    # Создать папку, если она не существует
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    google_crawler = GoogleImageCrawler(storage={'root_dir': storage_path})
    google_crawler.crawl(keyword=name, max_num=quantity)

    for item in parser.search(name, sizes=parser.size.medium):
        print(item.url)
        count += 1
        try:
            filename = wget.download(item.url, out=storage_path)
        except:
            continue

    # После загрузки фотографий можно сделать что-то с результатами, например, перейти к следующей строке в XLS файле.
