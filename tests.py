import unittest
import os
import shutil
from fs_operations import (
    list_files,
    create_folder,
    delete_folder,
    delete_file,
    move
)


class TestFileSystemOperations(unittest.TestCase):
    def setUp(self):
        # Создаем тестовые файлы и папки для всех тестов
        self.test_dir = 'test_dir'
        self.test_file = 'test_file.txt'
        self.moved_file = 'moved_file.txt'
        self.moved_dir = 'moved_dir'

        # Создаем папку
        os.makedirs(self.test_dir, exist_ok=True)

        # Создаем файл внутри директории
        with open(self.test_file, 'w') as f:
            f.write('Тестовый файл')

        # Создаем еще один файл внутри папки
        with open(os.path.join(self.test_dir, 'file_in_dir.txt'), 'w') as f:
            f.write('Тест внутри папки')

    def tearDown(self):
        # Удаляем все созданные файлы и папки после тестов
        for path in [self.test_file, self.moved_file]:
            if os.path.exists(path):
                os.remove(path)
        for path in [self.test_dir, self.moved_dir]:
            if os.path.exists(path):
                shutil.rmtree(path)

    def test_list_files(self):
        files = list_files(self.test_dir)
        self.assertIn('file_in_dir.txt', files)
        self.assertIsInstance(files, list)

    def test_create_folder(self):
        new_folder = 'test_create_folder'
        create_folder(new_folder)
        self.assertTrue(os.path.isdir(new_folder))
        # Очистка
        os.rmdir(new_folder)

    def test_delete_folder(self):
        # Создадим папку для удаления
        folder_to_delete = 'folder_to_delete'
        os.makedirs(folder_to_delete)
        delete_folder(folder_to_delete)
        self.assertFalse(os.path.exists(folder_to_delete))

        # Попытка удалить несуществующую папку
        delete_folder('несуществующая_папка')  # не ожидается исключение

    def test_delete_file(self):
        test_filename = 'file_to_delete.txt'
        with open(test_filename, 'w') as f:
            f.write('Удаление файла')
        delete_file(test_filename)
        self.assertFalse(os.path.exists(test_filename))

        # Попытка удалить несуществующий файл
        delete_file('несуществующий_файл.txt')  # не ожидается исключение

    def test_move_file(self):
        # Переместим файл в новое место
        move(self.test_file, self.moved_file)
        self.assertTrue(os.path.exists(self.moved_file))
        self.assertFalse(os.path.exists(self.test_file))
        # Переместим папку
        move(self.test_dir, self.moved_dir)
        self.assertTrue(os.path.exists(self.moved_dir))
        self.assertFalse(os.path.exists(self.test_dir))
        # Проверяем содержимое перемещенной папки
        self.assertTrue(os.path.exists(os.path.join(self.moved_dir, 'file_in_dir.txt')))

    def test_move_nonexistent(self):
        # Передача несуществующего файла
        move('nonexistent.txt', 'dest.txt')  # не вызывает ошибок

    def test_delete_nonexistent_file(self):
        # Удаление несуществующего файла не должно падать
        delete_file('nonexistent.txt')  # не вызывает ошибок

    def test_delete_nonexistent_folder(self):
        # Удаление несуществующей папки не должно падать
        delete_folder('nonexistent_folder')  # не вызывает ошибок


if __name__ == '__main__':
    unittest.main()