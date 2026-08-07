import unittest
import os
import shutil
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


class TestFileSystemOperations(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_dir'
        self.test_file = 'test_file.txt'
        self.moved_file = 'moved_file.txt'
        self.moved_dir = 'moved_dir'
        self.copied_file = 'copied_file.txt'
        self.copied_dir = 'copied_dir'

        os.makedirs(self.test_dir, exist_ok=True)

        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('Тестовый файл')

        with open(os.path.join(self.test_dir, 'file_in_dir.txt'), 'w', encoding='utf-8') as f:
            f.write('Тест внутри папки')

    def tearDown(self):
        for path in [self.test_file, self.moved_file, self.copied_file]:
            if os.path.exists(path):
                os.remove(path)
        for path in [self.test_dir, self.moved_dir, self.copied_dir]:
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
        os.rmdir(new_folder)

    def test_delete_folder(self):
        folder_to_delete = 'folder_to_delete'
        os.makedirs(folder_to_delete, exist_ok=True)
        with open(os.path.join(folder_to_delete, 'inside.txt'), 'w') as f:
            f.write('content')

        delete_folder(folder_to_delete)
        self.assertFalse(os.path.exists(folder_to_delete))
        delete_folder('несуществующая_папка')

    def test_delete_file(self):
        test_filename = 'file_to_delete.txt'
        with open(test_filename, 'w') as f:
            f.write('Удаление файла')
        delete_file(test_filename)
        self.assertFalse(os.path.exists(test_filename))
        delete_file('несуществующий_файл.txt')

    def test_move_file(self):
        move(self.test_file, self.moved_file)
        self.assertTrue(os.path.exists(self.moved_file))
        self.assertFalse(os.path.exists(self.test_file))
        move(self.test_dir, self.moved_dir)
        self.assertTrue(os.path.exists(self.moved_dir))
        self.assertFalse(os.path.exists(self.test_dir))
        self.assertTrue(os.path.exists(os.path.join(self.moved_dir, 'file_in_dir.txt')))

    def test_copy_file_and_folder(self):
        copy(self.test_file, self.copied_file)
        self.assertTrue(os.path.exists(self.copied_file))
        self.assertTrue(os.path.exists(self.test_file))

        copy(self.test_dir, self.copied_dir)
        self.assertTrue(os.path.exists(self.copied_dir))
        self.assertTrue(os.path.exists(os.path.join(self.copied_dir, 'file_in_dir.txt')))

    def test_search_a_like(self):
        results = search_a_like(self.test_dir, r'file_.*\.txt')
        self.assertEqual(len(results), 1)

    def test_append_date_to_files(self):
        date_dir = 'test_date_dir'
        os.makedirs(date_dir, exist_ok=True)
        file_path = os.path.join(date_dir, 'sample.txt')
        with open(file_path, 'w') as f:
            f.write('hello')
        append_date_to_files(date_dir)
        files = os.listdir(date_dir)
        self.assertTrue(any('sample_' in f for f in files))
        shutil.rmtree(date_dir)

    def test_analyse(self):
        total_size, items = analyse(self.test_dir)
        self.assertGreater(total_size, 0)
        self.assertEqual(len(items), 1)

    def test_move_nonexistent(self):
        move('nonexistent.txt', 'dest.txt')

    def test_delete_nonexistent_file(self):
        delete_file('nonexistent.txt')

    def test_delete_nonexistent_folder(self):
        delete_folder('nonexistent_folder')


if __name__ == '__main__':
    unittest.main()