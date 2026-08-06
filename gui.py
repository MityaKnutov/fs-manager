import flet as ft
import traceback

from fs_operations import (
    list_files,
    create_folder,
    delete_folder,
    delete_file,
    move,
    search_a_like,
    append_date_to_files
)

def main(page: ft.Page):
    page.title = "Файловый менеджер"
    page.vertical_alignment = ft.MainAxisAlignment.START

    output = ft.TextField(value="", width=500, height=300, multiline=True, read_only=True)

    def show_error(_e):
        output.value = f"Ошибка:\n{str(_e)}\n{traceback.format_exc()}"
        page.update()

    def list_dir(_e):
        try:
            from tkinter import filedialog
            dir_dialog = filedialog.askdirectory()
            if not dir_dialog:
                return
            result = list_files(dir_dialog)
            output.value = "\n".join(result)
            page.update()
        except Exception as e:
            show_error(e)

    def create_folder_click(_e):
        try:
            from tkinter import simpledialog
            folder_name = simpledialog.askstring("Создать папку", "Введите имя папки:")
            if folder_name:
                create_folder(folder_name)
                output.value = f"Папка '{folder_name}' создана"
                page.update()
        except Exception as e:
            show_error(e)

    def delete_folder_click(_e):
        try:
            from tkinter import simpledialog
            folder_name = simpledialog.askstring("Удалить папку", "Введите имя папки для удаления:")
            if folder_name:
                delete_folder(folder_name)
                output.value = f"Папка '{folder_name}' удалена"
                page.update()
        except Exception as e:
            show_error(e)

    def delete_file_click(_e):
        try:
            from tkinter import simpledialog
            file_path = simpledialog.askstring("Удалить файл", "Введите путь к файлу для удаления:")
            if file_path:
                delete_file(file_path)
                output.value = f"Файл '{file_path}' удален"
                page.update()
        except Exception as e:
            show_error(e)

    def move_file_click(_e):
        try:
            from tkinter import simpledialog
            src = simpledialog.askstring("Переместить", "Путь исходного файла/папки:")
            dst = simpledialog.askstring("Переместить", "Путь назначения:")
            if src and dst:
                move(src, dst)
                output.value = f"{src} перемещен(а) в {dst}"
                page.update()
        except Exception as e:
            show_error(e)

    def find_files_click(_e):
        try:
            from tkinter import simpledialog
            directory = simpledialog.askstring("Поиск файлов", "Каталог для поиска:")
            pattern = simpledialog.askstring("Поиск файлов", "Регулярное выражение:")
            if directory and pattern:
                result = search_a_like(directory, pattern)
                if result:
                    output.value = "\n".join(result)
                else:
                    output.value = "Файлы не найдены."
                page.update()
        except Exception as e:
            show_error(e)

    def add_date_click(_e):
        try:
            from tkinter import simpledialog
            path = simpledialog.askstring("Добавление даты", "Путь к папке/файлу:")
            recursive = False
            if path:
                # Спрашиваем про --recursive
                from tkinter import messagebox
                if messagebox.askyesno("Рекурсия", "Обработать все вложения?"):
                    recursive = True
                append_date_to_files(path, recursive)
                output.value = "Добавление даты завершено"
                page.update()
        except Exception as e:
            show_error(e)

    btn_list = ft.Button("Показать список", on_click=list_dir)
    btn_create = ft.Button("Создать папку", on_click=create_folder_click)
    btn_delete_folder = ft.Button("Удалить папку", on_click=delete_folder_click)
    btn_delete_file = ft.Button("Удалить файл", on_click=delete_file_click)
    btn_move = ft.Button("Переместить", on_click=move_file_click)
    btn_find = ft.Button("Поиск по шаблону", on_click=find_files_click)
    btn_add_date = ft.Button("Добавить дату к файлам", on_click=add_date_click)

    container = ft.Column([
        ft.Row([btn_list,btn_find]),
        ft.Row([btn_create, btn_delete_folder]),
        ft.Row([btn_delete_file, btn_move]),
        ft.Row([btn_add_date]),
        output
    ], spacing=5)

    page.add(container)

if __name__ == "__main__":
    ft.run(main)