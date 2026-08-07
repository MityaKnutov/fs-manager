import os
import logging
import shutil
import re
import datetime


def list_files(path='.'):
    try:
        files = os.listdir(path)
        print(f'Файлы в {path}:')
        for f in files:
            print(f'- {f}')
        return files
    except FileNotFoundError:
        print(f'Путь {path} не найден.')
        return []
    except Exception as e:
        logging.error(f'Ошибка при списке файлов: {e}')
        return []


def create_folder(folder_name, path='.'):
    try:
        full_path = os.path.join(path, folder_name)
        os.makedirs(full_path, exist_ok=True)
        print(f'Папка {full_path} создана.')
    except Exception as e:
        logging.error(f'Ошибка при создании папки: {e}')


def delete_folder(folder_name, path=None):
    try:
        if path is not None and path != '.':
            if os.path.exists(os.path.join(path, folder_name)):
                full_path = os.path.join(path, folder_name)
            elif os.path.exists(folder_name):
                full_path = folder_name
            elif os.path.exists(path):
                full_path = path
            else:
                full_path = os.path.join(path, folder_name)
        else:
            full_path = folder_name

        if not os.path.exists(full_path):
            print(f'Папка {full_path} не найдена.')
            return

        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f'Папка {full_path} удалена.')
        elif os.path.isfile(full_path):
            os.remove(full_path)
            print(f'Файл {full_path} удален.')
    except FileNotFoundError:
        print(f'Папка {folder_name} не найдена.')
    except Exception as e:
        logging.error(f'Ошибка при удалении папки: {e}')


def delete_file(file_path):
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
    try:
        shutil.move(source_path, destination_path)
        print(f'{source_path} успешно перемещен(а) в {destination_path}.')
    except FileNotFoundError:
        print(f'Источник {source_path} не найден.')
    except Exception as e:
        logging.error(f'Ошибка при перемещении файла: {e}')


def copy(source_path, destination_path):
    try:
        if not os.path.exists(source_path):
            print(f'Источник {source_path} не найден.')
            return
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
            print(f'{source_path} успешно скопирован(а) в {destination_path}.')
        else:
            shutil.copy2(source_path, destination_path)
            print(f'{source_path} успешно скопирован(а) в {destination_path}.')
    except FileNotFoundError:
        print(f'Источник {source_path} не найден.')
    except Exception as e:
        logging.error(f'Ошибка при копировании: {e}')


def search_a_like(directory, pattern):
    matched_files = []
    regex = re.compile(pattern)
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if regex.search(filename):
                matched_files.append(os.path.join(root, filename))
    return matched_files


def append_date_to_files(path, recursive=False):
    if not os.path.exists(path):
        print(f"Путь {path} не найден.")
        return

    if os.path.isfile(path):
        _append_date_to_file(path)
    elif os.path.isdir(path):
        if recursive:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    full_path = os.path.join(root, filename)
                    _append_date_to_file(full_path)
        else:
            for filename in os.listdir(path):
                full_path = os.path.join(path, filename)
                if os.path.isfile(full_path):
                    _append_date_to_file(full_path)


def _append_date_to_file(file_path):
    try:
        timestamp = os.path.getctime(file_path)
        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        dir_name, base_name = os.path.split(file_path)
        name, ext = os.path.splitext(base_name)
        new_name = f"{name}_{date_str}{ext}"
        new_path = os.path.join(dir_name, new_name)
        os.rename(file_path, new_path)
        print(f"Файл {file_path} переименован в {new_path}")
    except Exception as e:
        print(f"Ошибка при переименовании файла {file_path}: {e}")


def _get_path_size(p):
    if os.path.isfile(p) or os.path.islink(p):
        return os.path.getsize(p)
    total = 0
    for root, dirs, files in os.walk(p):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total


def format_size(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val}b"
    for unit in ['kb', 'mb', 'gb', 'tb']:
        bytes_val /= 1024.0
        if bytes_val < 1024 or unit == 'tb':
            val_str = f"{bytes_val:.1f}".rstrip('0').rstrip('.')
            return f"{val_str}{unit}"
    return f"{bytes_val}b"


def analyse(path='.'):
    if not os.path.exists(path):
        print(f'Путь {path} не найден.')
        return 0, []

    total_size = _get_path_size(path)
    print(f"full size: {format_size(total_size)}")

    items_info = []
    try:
        entries = sorted(os.listdir(path))
        for entry in entries:
            entry_path = os.path.join(path, entry)
            entry_size = _get_path_size(entry_path)
            formatted = format_size(entry_size)
            print(f"- {entry:<20} {formatted}")
            items_info.append((entry, entry_size))
    except Exception as e:
        logging.error(f'Ошибка при анализе директории: {e}')

    return total_size, items_info