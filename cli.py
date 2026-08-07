import logging
from fs_operations import (
    list_files,
    create_folder,
    delete_folder,
    delete_file,
    move,
    copy,
    search_a_like,
    append_date_to_files,
    analyse
)


def handle_command(command, params):
    try:
        if command == 'help':
            print_help()
        elif command == 'list':
            path = params[0] if params else '.'
            list_files(path)
        elif command == 'create':
            if len(params) < 1:
                print('Использование: create <folder_name> [path]')
                return
            folder_name = params[0]
            path = params[1] if len(params) > 1 else '.'
            create_folder(folder_name, path)
        elif command == 'delete':
            if len(params) < 1:
                print('Использование: delete <folder_name> [path]')
                return
            folder_name = params[0]
            path = params[1] if len(params) > 1 else '.'
            delete_folder(folder_name, path)
        elif command == 'delete_file':
            if len(params) != 1:
                print('Использование: delete_file <file_path>')
                return
            delete_file(params[0])
        elif command == 'move':
            if len(params) != 2:
                print('Использование: move <source_path> <destination_path>')
                return
            move(params[0], params[1])
        elif command == 'copy':
            if len(params) != 2:
                print('Использование: copy <source_path> <destination_path>')
                return
            copy(params[0], params[1])
        elif command == 'search_a_like':
            if len(params) != 2:
                print('Использование: search_a_like <directory> <regex_pattern>')
                return
            directory = params[0]
            pattern = params[1]
            find_results = search_a_like(directory, pattern)
            if find_results:
                print('Найденные файлы:')
                for file_path in find_results:
                    print(file_path)
            else:
                print('Файлы по шаблону не найдены.')
        elif command == 'add_date':
            if len(params) < 1:
                print('Использование: add_date <path> [--recursive]')
                return
            path = params[0]
            recursive = '--recursive' in params
            append_date_to_files(path, recursive)
        elif command in ('analyse', 'analyze'):
            path = params[0] if params else '.'
            analyse(path)
        else:
            print('Неизвестная команда')
    except Exception as e:
        logging.error(f'Ошибка выполнения команды: {e}')


def print_help():
    help_text = """
    Доступные команды:
    help - показать это сообщение
    list [directory] - список файлов в директории (по умолчанию текущая)
    create <folder_name> [path] - создать папку
    delete <folder_name> [path] - удалить папку (включая непустую)
    delete_file <path> - удалить файл
    move <source_path> <destination_path> - переместить файл или папку
    copy <source_path> <destination_path> - скопировать файл или папку
    search_a_like <directory> <regex_pattern> - поиск файлов по шаблону regex
    add_date <path> [--recursive] - добавить дату создания к имени файла
    analyse [directory] - анализ размера всех вложенных файлов и папок
    """
    print(help_text)