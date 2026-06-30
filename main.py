import argparse
import sys
import logging
from cli import handle_command


def main():
    parser = argparse.ArgumentParser(description='Простой файловый менеджер')
    parser.add_argument('command', help='Команда для выполнения', choices=['list', 'create', 'delete', 'help', 'move', 'delete_file', 'search_a_like', 'add_date'])
    parser.add_argument('params', nargs='*', help='Параметры команды')

    #Проверка наличия аргументов
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Настройка логирования
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Обработка команды
    handle_command(args.command, args.params)


if __name__ == '__main__':
    main()