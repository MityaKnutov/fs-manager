import logging
from fs_operations import list_files, create_folder, delete_folder

def handle_command(command, params):
    try:
        if command == 'help':
            print_help()
        elif command == 'list':
            path = params[0] if params else '.'
            list_files(path)
        elif command == 'create':
            if len(params) != 2:
                print('Использование: create <folder_name> <path>')
                return
            folder_name, path = params
            create_folder(folder_name, path)
        elif command == 'delete':
            if len(params) != 2:
                print('Использование: delete <folder_name> <path>')
                return
            folder_name, path = params
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
            move_file(params[0], params[1])
        else:
            print('Неизвестная команда')
    except Exception as e:
        logging.error(f'Ошибка выполнения команды: {e}')

def print_help():
    help_text = """
    Доступные команды:
    help - показать это сообщение
    list <directory> - список файлов в директории (по умолчанию текущая)
    create <folder_name> <path> - создать папку
    delete <folder_name> <path> - удалить папку
    move <name> <paths> - перемещает файл или папку
    delete_file <path> - удаляет файл по указанному пути
    """
    print(help_text)