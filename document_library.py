import flet as ft
import os
import subprocess
import platform
from pathlib import Path
from config import ALLOWED_EXTENSIONS

LIBRARY_PATH = "document_library"  # Папка для хранения документов

if not os.path.exists(LIBRARY_PATH):
    os.makedirs(LIBRARY_PATH)


class DocumentLibrary:
    def __init__(self, page: ft.Page, print_document_func):
        """
        Инициализация библиотеки документов

        Args:
            page (ft.Page): Страница Flet приложения
            print_document_func (function): Функция для печати документа
        """
        self.page = page
        self.print_document = print_document_func
        self.search_field = None
        self.file_list = None

    def add_file_to_library(self, file_path):
        """
        Добавляет файл в библиотеку документов

        Args:
            file_path (str): Путь к исходному файлу
        """
        file_name = os.path.basename(file_path)
        destination = os.path.join(LIBRARY_PATH, file_name)

        try:
            # Копируем файл в библиотеку
            with open(file_path, 'rb') as src_file:
                with open(destination, 'wb') as dst_file:
                    dst_file.write(src_file.read())

            self.page.snack_bar = ft.SnackBar(ft.Text(f"Файл {file_name} сохранен в библиотеку"))
            self.page.snack_bar.open = True

            # Обновляем список файлов, если открыто представление библиотеки
            if self.file_list:
                self.load_library_files()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка при сохранении файла: {str(ex)}"))
            self.page.snack_bar.open = True

        self.page.update()

    def open_file(self, file_name):
        """
        Открывает файл в программе по умолчанию для просмотра

        Args:
            file_name (str): Имя файла в библиотеке
        """
        file_path = os.path.join(LIBRARY_PATH, file_name)
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(['open', file_path])
            else:  # Linux и другие Unix-подобные системы
                subprocess.call(['xdg-open', file_path])

            self.page.snack_bar = ft.SnackBar(ft.Text(f"Открытие файла {file_name}"))
            self.page.snack_bar.open = True
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка при открытии файла: {str(ex)}"))
            self.page.snack_bar.open = True
        self.page.update()

    def print_library_file(self, file_name):
        """
        Отображает диалог печати для файла из библиотеки

        Args:
            file_name (str): Имя файла в библиотеке
        """

        def start_printing(e):
            file_path = os.path.join(LIBRARY_PATH, file_name)
            try:
                copies = int(copies_field.value)
                if copies < 1:
                    raise ValueError
                self.print_document(file_path, copies)
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Документ {file_name} отправлен на печать ({copies} копий)"))
                self.page.snack_bar.open = True
                self.close_dialog()
            except ValueError:
                self.page.snack_bar = ft.SnackBar(ft.Text("Ошибка: введите корректное число копий"))
                self.page.snack_bar.open = True
                self.page.update()

        copies_field = ft.TextField(label="Количество копий", value="1", width=100)

        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Параметры печати"),
            content=ft.Column([
                ft.Text(f"Файл: {file_name}"),
                copies_field
            ]),
            actions=[
                ft.TextButton("Распечатать", on_click=start_printing),
                ft.TextButton("Отмена", on_click=self.close_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Закрывает активный диалог"""
        self.page.dialog.open = False
        self.page.update()

    def show_file_options(self, file_name):
        """
        Отображает диалог с действиями для файла

        Args:
            file_name (str): Имя файла в библиотеке
        """

        def close_dialog():
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = ft.AlertDialog(
            title=ft.Text(file_name),
            content=ft.Column([
                ft.Text("Выберите действие:")
            ]),
            actions=[
                ft.TextButton("Открыть", on_click=lambda _: (close_dialog(), self.open_file(file_name))),
                ft.TextButton("Печать", on_click=lambda _: (close_dialog(), self.print_library_file(file_name))),
                ft.TextButton("Отмена", on_click=close_dialog)
            ]
        )
        self.page.dialog.open = True
        self.page.update()

    def load_library_files(self, search_term=""):
        """
        Загружает список файлов из библиотеки

        Args:
            search_term (str): Строка для поиска файлов
        """
        if not self.file_list:
            return

        self.file_list.controls.clear()

        try:
            files = os.listdir(LIBRARY_PATH)
            matching_files = [f for f in files if search_term.lower() in f.lower() and
                              os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]

            if matching_files:
                for file in matching_files:
                    icon = ft.Icon(ft.icons.PICTURE_AS_PDF if file.lower().endswith('.pdf') else ft.icons.DESCRIPTION)
                    self.file_list.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Row([
                                    icon,
                                    ft.Text(file, size=16, expand=True),
                                    ft.IconButton(
                                        icon=ft.icons.OPEN_IN_NEW,
                                        on_click=lambda e, f=file: self.open_file(f),
                                        tooltip="Открыть"
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.PRINT,
                                        on_click=lambda e, f=file: self.print_library_file(f),
                                        tooltip="Печать"
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                padding=10
                            ),
                            margin=5
                        )
                    )
            else:
                self.file_list.controls.append(
                    ft.Container(
                        content=ft.Text("Файлы не найдены", size=16, text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        margin=20
                    )
                )
        except Exception as e:
            self.file_list.controls.append(
                ft.Container(
                    content=ft.Text(f"Ошибка: {str(e)}", size=16, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.center,
                    margin=20
                )
            )

        self.page.update()

    def search_files(self, e):
        """Обработчик события поиска файлов"""
        if self.search_field:
            self.load_library_files(self.search_field.value)

    def create_view(self, go_back_route):
        """
        Создает представление библиотеки документов

        Args:
            go_back_route (str): Маршрут для кнопки "Назад"

        Returns:
            ft.View: Представление библиотеки документов
        """
        self.search_field = ft.TextField(label="Поиск по названию", expand=True)
        self.file_list = ft.ListView(expand=True, spacing=10, padding=20)

        self.load_library_files()

        return ft.View(
            "/document_library",
            controls=[
                ft.Text("Библиотека документов", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    self.search_field,
                    ft.IconButton(
                        icon=ft.icons.SEARCH,
                        on_click=self.search_files,
                        tooltip="Поиск"
                    ),
                ], spacing=10),
                ft.Divider(),
                ft.Container(
                    content=self.file_list,
                    expand=True
                ),
                ft.Row([
                    ft.ElevatedButton(
                        "Назад",
                        on_click=lambda _: self.page.go(go_back_route),
                        icon=ft.icons.ARROW_BACK
                    ),
                ], alignment=ft.MainAxisAlignment.END, spacing=20),
            ],
            padding=20
        )


def get_library_files():
    """
    Получает список файлов в библиотеке документов

    Returns:
        list: Список файлов с допустимыми расширениями
    """
    if not os.path.exists(LIBRARY_PATH):
        return []
    return [f for f in os.listdir(LIBRARY_PATH) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]