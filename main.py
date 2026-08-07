import argparse
import sys
import logging
from cli import handle_command


def main():
    parser = argparse.ArgumentParser(description='Простой файловый менеджер')
    parser.add_argument('command', help='Команда для выполнения', choices=[
        'list', 'create', 'delete', 'help', 'move', 'copy',
        'delete_file', 'search_a_like', 'add_date', 'analyse', 'analyze'
    ])
    parser.add_argument('params', nargs='*', help='Параметры команды')

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    handle_command(args.command, args.params)


if __name__ == '__main__':
    main()