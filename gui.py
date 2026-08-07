import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import traceback

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


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify=tk.LEFT,
            background="#ffffe0", relief=tk.SOLID, borderwidth=1,
            font=("tahoma", "9", "normal")
        )
        label.pack(ipadx=5, ipady=3)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class FSManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Файловый менеджер")
        self.root.geometry("750x550")
        self.root.minsize(650, 450)

        self._create_widgets()

    def _create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tab_view = ttk.Frame(notebook)
        notebook.add(tab_view, text="Просмотр и Поиск")
        self._setup_view_tab(tab_view)

        tab_edit = ttk.Frame(notebook)
        notebook.add(tab_edit, text="Создание и Удаление")
        self._setup_edit_tab(tab_edit)

        tab_transfer = ttk.Frame(notebook)
        notebook.add(tab_transfer, text="Перемещение и Копирование")
        self._setup_transfer_tab(tab_transfer)

        tab_tools = ttk.Frame(notebook)
        notebook.add(tab_tools, text="Анализ и Даты")
        self._setup_tools_tab(tab_tools)

        output_frame = ttk.LabelFrame(self.root, text="Результат / Журнал операций")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=10)
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def clear_log(self):
        self.output_text.delete("1.0", tk.END)

    def safe_execute(self, action_func, success_message=None):
        try:
            result = action_func()
            if success_message:
                self.log(f"[УСПЕХ] {success_message}")
            return result
        except Exception as e:
            err_msg = f"[ОШИБКА] {str(e)}"
            self.log(err_msg)
            messagebox.showerror("Ошибка выполнения", f"Произошла ошибка:\n{str(e)}")

    def _setup_view_tab(self, parent):
        frame_list = ttk.LabelFrame(parent, text="Список файлов в директории")
        frame_list.pack(fill=tk.X, padx=10, pady=5)

        lbl_path = ttk.Label(frame_list, text="Путь:")
        lbl_path.pack(side=tk.LEFT, padx=5, pady=5)

        self.entry_list_path = ttk.Entry(frame_list, width=40)
        self.entry_list_path.insert(0, ".")
        self.entry_list_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ToolTip(self.entry_list_path, "Укажите путь или выберите папку через обзор")

        btn_browse = ttk.Button(frame_list, text="Обзор...", command=lambda: self._browse_dir(self.entry_list_path))
        btn_browse.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(btn_browse, "Выбрать папку для просмотра")

        btn_run_list = ttk.Button(frame_list, text="Показать файлы", command=self._action_list_files)
        btn_run_list.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(btn_run_list, "Вывести список файлов в указанной директории")

        frame_search = ttk.LabelFrame(parent, text="Поиск файлов по регулярному выражению (search_a_like)")
        frame_search.pack(fill=tk.X, padx=10, pady=5)

        lbl_s_dir = ttk.Label(frame_search, text="Папка:")
        lbl_s_dir.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_search_dir = ttk.Entry(frame_search, width=35)
        self.entry_search_dir.insert(0, ".")
        self.entry_search_dir.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_search_dir, "Каталог поиска")

        btn_s_browse = ttk.Button(frame_search, text="Обзор...", command=lambda: self._browse_dir(self.entry_search_dir))
        btn_s_browse.grid(row=0, column=2, padx=5, pady=5)

        lbl_regex = ttk.Label(frame_search, text="Regex шаблон:")
        lbl_regex.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_regex = ttk.Entry(frame_search, width=35)
        self.entry_regex.insert(0, r".*\.py$")
        self.entry_regex.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_regex, "Регулярное выражение (например, .*\\.py$ для всех Python файлов)")

        btn_search = ttk.Button(frame_search, text="Найти", command=self._action_search)
        btn_search.grid(row=1, column=2, padx=5, pady=5)
        ToolTip(btn_search, "Запустить поиск по указанному шаблону")

        frame_search.columnconfigure(1, weight=1)

    def _action_list_files(self):
        path = self.entry_list_path.get().strip() or "."
        def run():
            files = list_files(path)
            self.log(f"--- Файлы в {path} ---")
            for f in files:
                self.log(f" - {f}")
        self.safe_execute(run)

    def _action_search(self):
        directory = self.entry_search_dir.get().strip() or "."
        pattern = self.entry_regex.get().strip()
        if not pattern:
            messagebox.showwarning("Предупреждение", "Введите шаблон regex.")
            return
        def run():
            results = search_a_like(directory, pattern)
            self.log(f"--- Результаты поиска '{pattern}' в {directory} ---")
            if results:
                for r in results:
                    self.log(f" - {r}")
            else:
                self.log("Совпадающих файлов не найдено.")
        self.safe_execute(run)

    def _setup_edit_tab(self, parent):
        frame_create = ttk.LabelFrame(parent, text="Создать папку")
        frame_create.pack(fill=tk.X, padx=10, pady=5)

        lbl_c_name = ttk.Label(frame_create, text="Имя папки:")
        lbl_c_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_c_name = ttk.Entry(frame_create, width=25)
        self.entry_c_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_c_name, "Название создаваемой папки")

        lbl_c_path = ttk.Label(frame_create, text="Где создать:")
        lbl_c_path.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_c_path = ttk.Entry(frame_create, width=25)
        self.entry_c_path.insert(0, ".")
        self.entry_c_path.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_c_path, "Путь директории для создания")

        btn_c_browse = ttk.Button(frame_create, text="Обзор", command=lambda: self._browse_dir(self.entry_c_path))
        btn_c_browse.grid(row=0, column=4, padx=5, pady=5)

        btn_create = ttk.Button(frame_create, text="Создать", command=self._action_create_folder)
        btn_create.grid(row=0, column=5, padx=5, pady=5)
        ToolTip(btn_create, "Создать новую папку")

        frame_create.columnconfigure(1, weight=1)
        frame_create.columnconfigure(3, weight=1)

        frame_del_dir = ttk.LabelFrame(parent, text="Удалить папку (включая непустые)")
        frame_del_dir.pack(fill=tk.X, padx=10, pady=5)

        lbl_dd_name = ttk.Label(frame_del_dir, text="Папка:")
        lbl_dd_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_dd_name = ttk.Entry(frame_del_dir, width=35)
        self.entry_dd_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_dd_name, "Имя или путь папки для удаления")

        btn_dd_browse = ttk.Button(frame_del_dir, text="Обзор...", command=lambda: self._browse_dir(self.entry_dd_name))
        btn_dd_browse.grid(row=0, column=2, padx=5, pady=5)

        btn_del_dir = ttk.Button(frame_del_dir, text="Удалить папку", command=self._action_delete_folder)
        btn_del_dir.grid(row=0, column=3, padx=5, pady=5)
        ToolTip(btn_del_dir, "Удалить папку со всеми вложенными файлами")

        frame_del_dir.columnconfigure(1, weight=1)

        frame_del_file = ttk.LabelFrame(parent, text="Удалить файл")
        frame_del_file.pack(fill=tk.X, padx=10, pady=5)

        lbl_df_path = ttk.Label(frame_del_file, text="Файл:")
        lbl_df_path.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_df_path = ttk.Entry(frame_del_file, width=35)
        self.entry_df_path.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        ToolTip(self.entry_df_path, "Путь к удаляемому файлу")

        btn_df_browse = ttk.Button(frame_del_file, text="Обзор...", command=lambda: self._browse_file(self.entry_df_path))
        btn_df_browse.grid(row=0, column=2, padx=5, pady=5)

        btn_del_file = ttk.Button(frame_del_file, text="Удалить файл", command=self._action_delete_file)
        btn_del_file.grid(row=0, column=3, padx=5, pady=5)
        ToolTip(btn_del_file, "Удалить выбранный файл")

        frame_del_file.columnconfigure(1, weight=1)

    def _action_create_folder(self):
        folder_name = self.entry_c_name.get().strip()
        path = self.entry_c_path.get().strip() or "."
        if not folder_name:
            messagebox.showwarning("Предупреждение", "Введите имя создаваемой папки.")
            return
        def run():
            create_folder(folder_name, path)
            self.log(f"Папка '{folder_name}' создана в '{path}'")
        self.safe_execute(run)

    def _action_delete_folder(self):
        folder_name = self.entry_dd_name.get().strip()
        if not folder_name:
            messagebox.showwarning("Предупреждение", "Укажите папку для удаления.")
            return
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить папку '{folder_name}'?"):
            return
        def run():
            delete_folder(folder_name)
            self.log(f"Папка '{folder_name}' удалена.")
        self.safe_execute(run)

    def _action_delete_file(self):
        file_path = self.entry_df_path.get().strip()
        if not file_path:
            messagebox.showwarning("Предупреждение", "Укажите путь к файлу.")
            return
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить файл '{file_path}'?"):
            return
        def run():
            delete_file(file_path)
            self.log(f"Файл '{file_path}' удален.")
        self.safe_execute(run)

    def _setup_transfer_tab(self, parent):
        frame_move = ttk.LabelFrame(parent, text="Переместить (move)")
        frame_move.pack(fill=tk.X, padx=10, pady=5)

        lbl_m_src = ttk.Label(frame_move, text="Источник:")
        lbl_m_src.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_m_src = ttk.Entry(frame_move, width=30)
        self.entry_m_src.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        btn_m_src_b = ttk.Button(frame_move, text="Файл", command=lambda: self._browse_file(self.entry_m_src))
        btn_m_src_b.grid(row=0, column=2, padx=2, pady=5)
        btn_m_src_dir = ttk.Button(frame_move, text="Папка", command=lambda: self._browse_dir(self.entry_m_src))
        btn_m_src_dir.grid(row=0, column=3, padx=2, pady=5)

        lbl_m_dst = ttk.Label(frame_move, text="Назначение:")
        lbl_m_dst.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_m_dst = ttk.Entry(frame_move, width=30)
        self.entry_m_dst.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        btn_m_dst_b = ttk.Button(frame_move, text="Обзор", command=lambda: self._browse_dir(self.entry_m_dst))
        btn_m_dst_b.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        btn_move = ttk.Button(frame_move, text="Переместить", command=self._action_move)
        btn_move.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.EW)
        ToolTip(btn_move, "Переместить выбранный файл или папку")

        frame_move.columnconfigure(1, weight=1)

        frame_copy = ttk.LabelFrame(parent, text="Скопировать (copy)")
        frame_copy.pack(fill=tk.X, padx=10, pady=5)

        lbl_cp_src = ttk.Label(frame_copy, text="Источник:")
        lbl_cp_src.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_cp_src = ttk.Entry(frame_copy, width=30)
        self.entry_cp_src.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        btn_cp_src_b = ttk.Button(frame_copy, text="Файл", command=lambda: self._browse_file(self.entry_cp_src))
        btn_cp_src_b.grid(row=0, column=2, padx=2, pady=5)
        btn_cp_src_dir = ttk.Button(frame_copy, text="Папка", command=lambda: self._browse_dir(self.entry_cp_src))
        btn_cp_src_dir.grid(row=0, column=3, padx=2, pady=5)

        lbl_cp_dst = ttk.Label(frame_copy, text="Назначение:")
        lbl_cp_dst.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_cp_dst = ttk.Entry(frame_copy, width=30)
        self.entry_cp_dst.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        btn_cp_dst_b = ttk.Button(frame_copy, text="Обзор", command=lambda: self._browse_dir(self.entry_cp_dst))
        btn_cp_dst_b.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        btn_copy = ttk.Button(frame_copy, text="Скопировать", command=self._action_copy)
        btn_copy.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky=tk.EW)
        ToolTip(btn_copy, "Скопировать файл или директорию")

        frame_copy.columnconfigure(1, weight=1)

    def _action_move(self):
        src = self.entry_m_src.get().strip()
        dst = self.entry_m_dst.get().strip()
        if not src or not dst:
            messagebox.showwarning("Предупреждение", "Укажите источник и назначение.")
            return
        def run():
            move(src, dst)
            self.log(f"Объект '{src}' успешно перемещен в '{dst}'")
        self.safe_execute(run)

    def _action_copy(self):
        src = self.entry_cp_src.get().strip()
        dst = self.entry_cp_dst.get().strip()
        if not src or not dst:
            messagebox.showwarning("Предупреждение", "Укажите источник и назначение.")
            return
        def run():
            copy(src, dst)
            self.log(f"Объект '{src}' успешно скопирован в '{dst}'")
        self.safe_execute(run)

    def _setup_tools_tab(self, parent):
        frame_date = ttk.LabelFrame(parent, text="Добавление даты создания к имени файла (add_date)")
        frame_date.pack(fill=tk.X, padx=10, pady=5)

        lbl_d_path = ttk.Label(frame_date, text="Путь:")
        lbl_d_path.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_d_path = ttk.Entry(frame_date, width=30)
        self.entry_d_path.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        btn_d_file = ttk.Button(frame_date, text="Файл", command=lambda: self._browse_file(self.entry_d_path))
        btn_d_file.grid(row=0, column=2, padx=2, pady=5)
        btn_d_dir = ttk.Button(frame_date, text="Папка", command=lambda: self._browse_dir(self.entry_d_path))
        btn_d_dir.grid(row=0, column=3, padx=2, pady=5)

        self.var_recursive = tk.BooleanVar(value=False)
        chk_rec = ttk.Checkbutton(frame_date, text="Рекурсивно (все вложенные папки)", variable=self.var_recursive)
        chk_rec.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        btn_add_date = ttk.Button(frame_date, text="Добавить дату", command=self._action_add_date)
        btn_add_date.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=tk.EW)
        ToolTip(btn_add_date, "Переименовать файлы, добавив YYYYMMDD дату создания")

        frame_date.columnconfigure(1, weight=1)

        frame_analyse = ttk.LabelFrame(parent, text="Анализ объемов директории (analyse)")
        frame_analyse.pack(fill=tk.X, padx=10, pady=5)

        lbl_a_path = ttk.Label(frame_analyse, text="Директория:")
        lbl_a_path.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry_a_path = ttk.Entry(frame_analyse, width=35)
        self.entry_a_path.insert(0, ".")
        self.entry_a_path.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        btn_a_browse = ttk.Button(frame_analyse, text="Обзор...", command=lambda: self._browse_dir(self.entry_a_path))
        btn_a_browse.pack(side=tk.LEFT, padx=5, pady=5)

        btn_analyse = ttk.Button(frame_analyse, text="Запустить анализ", command=self._action_analyse)
        btn_analyse.pack(side=tk.LEFT, padx=5, pady=5)
        ToolTip(btn_analyse, "Рассчитать объемы всех вложенных папок и файлов")

    def _action_add_date(self):
        path = self.entry_d_path.get().strip()
        if not path:
            messagebox.showwarning("Предупреждение", "Укажите файл или папку.")
            return
        rec = bool(self.var_recursive.get())
        def run():
            append_date_to_files(path, recursive=rec)
            self.log(f"Добавление даты для '{path}' завершено (рекурсия: {rec}).")
        self.safe_execute(run)

    def _action_analyse(self):
        path = self.entry_a_path.get().strip() or "."
        def run():
            total_size, items = analyse(path)
            self.log(f"--- Результаты анализа для '{path}' ---")
            self.log(f"Полный объем: {total_size} байт")
            for name, size in items:
                self.log(f" - {name:<25} {size} байт")
        self.safe_execute(run)

    def _browse_dir(self, target_entry):
        selected = filedialog.askdirectory()
        if selected:
            target_entry.delete(0, tk.END)
            target_entry.insert(0, selected)

    def _browse_file(self, target_entry):
        selected = filedialog.askopenfilename()
        if selected:
            target_entry.delete(0, tk.END)
            target_entry.insert(0, selected)


def main():
    root = tk.Tk()
    app = FSManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()