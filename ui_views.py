import flet as ft
import os
from config import MAIN_BUTTON_STYLE


class UIViews:
    """Класс для создания UI представлений приложения"""

    def __init__(self, page, go_back_handler, theme_handler, usb_service, printer_service):
        """
        Инициализация класса представлений

        Args:
            page (ft.Page): Страница Flet приложения
            go_back_handler (function): Функция для возврата на предыдущую страницу
            theme_handler (function): Функция для изменения темы
            usb_service (USBService): Сервис для работы с USB
            printer_service (PrinterService): Сервис для работы с принтерами
        """
        self.page = page
        self.go_back = go_back_handler
        self.change_theme = theme_handler
        self.usb_service = usb_service
        self.printer_service = printer_service

        # Создаем стиль кнопок из конфигурации
        self.button_style = {
            "width": MAIN_BUTTON_STYLE["width"],
            "height": MAIN_BUTTON_STYLE["height"],
            "style": ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=18),
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE
            ),
        }

    def main_view(self):
        """Главное представление приложения"""
        return ft.View(
            "/",
            controls=[
                ft.Text("KazTypo", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=self.change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Распечатать\n Документ", on_click=lambda _: self.page.go("/print"),
                                      **self.button_style),
                    ft.ElevatedButton("Копировать\n Документ", on_click=lambda _: self.page.go("/copy"),
                                      **self.button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Сканировать\n  Документ", on_click=lambda _: self.page.go("/scan"),
                                      **self.button_style),
                    ft.ElevatedButton("Разместить рекламу", on_click=lambda _: self.page.go("/advertising"),
                                      **self.button_style)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Узнать цену", on_click=lambda _: self.page.go("/price"), width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def print_view(self):
        """Представление меню печати"""
        return ft.View(
            "/print",
            controls=[
                ft.Text("Выберите способ печати", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=self.change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Печать с USB", on_click=lambda _: self.page.go("/print_usb"),
                                      **self.button_style),
                    ft.ElevatedButton("Печать с Telegram", **self.button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Библиотека документов", on_click=lambda _: self.page.go("/document_library"),
                                      **self.button_style),
                    ft.ElevatedButton("Распечатать с веб-сервиса", **self.button_style)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=self.go_back, width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def copy_view(self):
        """Представление копирования документа"""
        return ft.View(
            "/copy",
            controls=[
                ft.Text("Как правильно копировать документ", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "1. Вставьте документ в лоток\n2. Выберите нужные параметры\n3. Нажмите 'Оплатить' для начала копирования"),
                ft.ElevatedButton("Оплатить"),
                ft.ElevatedButton("Назад", on_click=self.go_back),
            ]
        )

    def scan_view(self):
        """Представление сканирования документа"""
        return ft.View(
            "/scan",
            controls=[
                ft.Text("Выберите способ сканирования", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=self.change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Отсканировать на флешку", **self.button_style),
                    ft.ElevatedButton("Отсканировать в Telegram", **self.button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=self.go_back, width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def price_view(self):
        """Представление цен на услуги"""
        return ft.View(
            "/price",
            controls=[
                ft.Text("Цены на услуги", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("1. Печать - от 50 тг\n2. Копирование - от 30 тг\n3. Сканирование - от 40 тг"),
                ft.ElevatedButton("Назад", on_click=self.go_back),
            ]
        )

    def advertising_view(self):
        """Представление размещения рекламы"""
        return ft.View(
            "/advertising",
            controls=[
                ft.Text("Разместить рекламу", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Для размещения рекламы свяжитесь с нами по телефону: +7 (123) 456-78-90"),
                ft.ElevatedButton("Назад", on_click=self.go_back),
            ]
        )

    def print_usb_view(self, print_document_handler, save_to_library_handler):
        """
        Представление печати с USB

        Args:
            print_document_handler (function): Функция для печати документа
            save_to_library_handler (function): Функция для сохранения в библиотеку
        """
        file_list = ft.Column()
        copies_field = ft.TextField(label="Количество копий", value="1", width=100)
        selected_file = ft.Text()

        def check_usb(e):
            drives = self.usb_service.get_usb_drives()
            file_list.controls.clear()
            if drives:
                usb_drive = drives[0]
                files = self.usb_service.list_files_in_usb(usb_drive)
                if files:
                    for file in files:
                        file_list.controls.append(
                            ft.TextButton(
                                text=file,
                                on_click=lambda e, f=file: show_print_dialog(f, usb_drive)
                            )
                        )
                else:
                    file_list.controls.append(ft.Text("Файлы не найдены", size=16))
            else:
                file_list.controls.append(ft.Text("Флешка не найдена", size=16))
            self.page.update()

        def show_print_dialog(file, usb_drive):
            selected_file.value = file

            def start_printing(e):
                file_path = os.path.join(usb_drive, file)
                try:
                    copies = int(copies_field.value)
                    if copies < 1:
                        raise ValueError
                    print_document_handler(file_path, copies)
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"Документ {file} отправлен на печать ({copies} копий)"))
                    self.page.snack_bar.open = True
                    close_dialog()
                except ValueError:
                    self.page.snack_bar = ft.SnackBar(ft.Text("Ошибка: введите корректное число копий"))
                    self.page.snack_bar.open = True
                    self.page.update()

            def save_to_library(e):
                file_path = os.path.join(usb_drive, file)
                save_to_library_handler(file_path)
                close_dialog()

            def close_dialog():
                self.page.dialog.open = False
                self.page.update()

            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Параметры печати"),
                content=ft.Column([
                    ft.Text(f"Файл: {file}"),
                    copies_field
                ]),
                actions=[
                    ft.TextButton("Распечатать", on_click=start_printing),
                    ft.TextButton("Сохранить в библиотеку", on_click=save_to_library),
                    ft.TextButton("Отмена", on_click=close_dialog)
                ]
            )
            self.page.dialog.open = True
            self.page.update()

        return ft.View(
            "/print_usb",
            controls=[
                ft.Text("Печать с USB", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton("Обнаружить USB", on_click=check_usb),
                file_list,
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=lambda _: self.page.go("/print"), width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )