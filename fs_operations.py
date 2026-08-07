import os
import logging
import shutil
import re

def list_files(path='.'):
    try:
        files = os.listdir(path)
        print(f'Файлы в {path}:')
        for f in files:
            print(f'- {f}')
        return files  # добавьте возврат списка
    except FileNotFoundError:
        print(f'Путь {path} не найден.')
        return []
    except Exception as e:
        logging.error(f'Ошибка при списке файлов: {e}')
        return []

def create_folder(folder_name, path='.'):
    #Создает папку
    try:
        full_path = os.path.join(path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        print(f'Папка {full_path} создана.')
    except Exception as e:
        logging.error(f'Ошибка при создании папки: {e}')

def delete_folder(folder_name, path='.'):
    #Удаляет папку
    try:
        full_path = os.path.join(path, folder_name)
        os.rmdir(full_path)
        print(f'Папка {full_path} удалена.')
    except FileNotFoundError:
        print(f'Папка {full_path} не найдена.')
    except OSError:
        print(f'Папка {full_path} не пуста или не может быть удалена.')
    except Exception as e:
        logging.error(f'Ошибка при удалении папки: {e}')

def delete_file(file_path):
    #Удаляет файл по указанному пути
    try:
        os.remove(file_path)
        print(f'Файл {file_path} удален.')
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
    except IsADirectoryError:
        print(f'{file_path} — это папка, а не файл.')
    except Exception as e:
        logging.error(f'Ошибка при удалении файла: {e}')

def move(source_path, destination_path):
    #Перемещает файл или папку
    try:
        shutil.move(source_path, destination_path)
        print(f'{source_path} успешно перемещен(а) в {destination_path}.')
    except FileNotFoundError:
        print(f'Источник {source_path} не найден.')
    except Exception as e:
        logging.error(f'Ошибка при перемещении файла: {e}')

def search_a_like(directory, pattern):
    '''Поиск файлов в папках, в том числе во вложенных, соответствующих шаблону regex.
    :param directory: путь к каталогу
    :param pattern: строка regex
    :return: список путей найденных файлов
    '''
    matched_files = []
    regex = re.compile(pattern)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if regex.search(filename):
                matched_files.append(os.path.join(root, filename))
    return matched_files