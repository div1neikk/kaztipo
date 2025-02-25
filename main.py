import flet as ft
import win32print
import win32ui
import os
import psutil


ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}

def main(page: ft.Page):
    page.title = "divine prod"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 700
    page.window.height = 1020

    button_style = {
        "width": 310,
        "height": 350,
        "style": ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=18),
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE
        ),
    }

    def get_usb_drives():
        drives = []
        for part in psutil.disk_partitions():
            if "removable" in part.opts or (
                    "cdrom" not in part.opts and part.device.startswith(("/dev/sd", "E:", "F:", "G:"))):
                drives.append(part.device)
        return drives

    def list_files_in_usb(drive):
        try:
            return [f for f in os.listdir(drive) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
        except Exception as e:
            return []

    def get_printers():
        return [printer[2] for printer in win32print.EnumPrinters(2)]

    def print_document(file_path, copies):
        printer_name = win32print.GetDefaultPrinter()
        hprinter = win32print.OpenPrinter(printer_name)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(printer_name)

        pdc.StartDoc(file_path)
        for _ in range(copies):
            pdc.StartPage()
            pdc.TextOut(100, 100, f"Печать: {os.path.basename(file_path)}")
            pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(main_view())
        elif page.route == "/print":
            page.views.append(print_view())
        elif page.route == "/copy":
            page.views.append(copy_view())
        elif page.route == "/scan":
            page.views.append(scan_view())
        elif page.route == "/price":
            page.views.append(price_view())
        elif page.route == "/advertising":
            page.views.append(advertising_view())
        elif page.route == "/print_usb":
            page.views.append(print_usb_view())
        page.update()

    def go_back(e):
        page.go("/")

    def main_view():
        return ft.View(
            "/",
            controls=[
                ft.Text("KazTypo", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Распечатать\n Документ", on_click=lambda _: page.go("/print"), **button_style),
                    ft.ElevatedButton("Копировать\n Документ", on_click=lambda _: page.go("/copy"), **button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Сканировать\n  Документ", on_click=lambda _: page.go("/scan"), **button_style),
                    ft.ElevatedButton("Разместить рекламу", on_click=lambda _: page.go("/advertising"), **button_style)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Узнать цену", on_click=lambda _: page.go("/price"), width=150, height = 50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def print_view():
        return ft.View(
            "/print",
            controls=[
                ft.Text("Выберите способ печати", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Печать с USB", on_click=lambda _: page.go("/print_usb"),**button_style),
                    ft.ElevatedButton("Печать с Telegram", **button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Библиотека документов",**button_style),
                    ft.ElevatedButton("Распечатать с веб-сервиса",**button_style)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=go_back, width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def copy_view():
        return ft.View(
            "/copy",
            controls=[
                ft.Text("Как правильно копировать документ", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("1. Вставьте документ в лоток\n2. Выберите нужные параметры\n3. Нажмите 'Оплатить' для начала копирования"),
                ft.ElevatedButton("Оплатить"),
                ft.ElevatedButton("Назад", on_click=go_back),
            ]
        )

    def scan_view():
        return ft.View(
            "/scan",
            controls=[
                ft.Text("Выберите способ сканирования", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(width=20),
                    ft.IconButton(ft.icons.SUNNY, icon_size=30, on_click=change_theme),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.ElevatedButton("Отсканировать на флешку", **button_style),
                    ft.ElevatedButton("Отсканировать в Telegram", **button_style),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=13),
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=go_back, width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )

    def price_view():
        return ft.View(
            "/price",
            controls=[
                ft.Text("Цены на услуги", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("1. Печать - от 50 тг\n2. Копирование - от 30 тг\n3. Сканирование - от 40 тг"),
                ft.ElevatedButton("Назад", on_click=go_back),
            ]
        )

    def advertising_view():
        return ft.View(
            "/advertising",
            controls=[
                ft.Text("Разместить рекламу", size=20, weight=ft.FontWeight.BOLD),
                ft.Text("Для размещения рекламы свяжитесь с нами по телефону: +7 (123) 456-78-90"),
                ft.ElevatedButton("Назад", on_click=go_back),
            ]
        )

    def print_usb_view():
        file_list = ft.Column()
        copies_field = ft.TextField(label="Количество копий", value="1", width=100)
        selected_file = ft.Text()

        def check_usb(e):
            drives = get_usb_drives()
            file_list.controls.clear()
            if drives:
                usb_drive = drives[0]
                files = list_files_in_usb(usb_drive)
                if files:
                    for file in files:
                        file_list.controls.append(
                            ft.TextButton(text=file, on_click=lambda e, f=file: show_print_dialog(f, usb_drive)))
                else:
                    file_list.controls.append(ft.Text("Файлы не найдены", size=16))
            else:
                file_list.controls.append(ft.Text("Флешка не найдена", size=16))
            page.update()

        def show_print_dialog(file, usb_drive):
            selected_file.value = file

            def start_printing(e):
                file_path = os.path.join(usb_drive, file)
                try:
                    copies = int(copies_field.value)
                    if copies < 1:
                        raise ValueError
                    print_document(file_path, copies)
                    page.snack_bar = ft.SnackBar(ft.Text(f"Документ {file} отправлен на печать ({copies} копий)"))
                    page.snack_bar.open = True
                    close_dialog()
                except ValueError:
                    page.snack_bar = ft.SnackBar(ft.Text("Ошибка: введите корректное число копий"))
                    page.snack_bar.open = True
                    page.update()

            def close_dialog():
                page.dialog.open = False
                page.update()

            page.dialog = ft.AlertDialog(
                title=ft.Text("Параметры печати"),
                content=ft.Column([
                    ft.Text(f"Файл: {file}"),
                    copies_field
                ]),
                actions=[
                    ft.TextButton("Распечатать", on_click=start_printing),
                    ft.TextButton("Отмена", on_click=close_dialog)
                ]
            )
            page.dialog.open = True
            page.update()

        return ft.View(
            "/print_usb",
            controls=[
                ft.Text("Печать с USB", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.ElevatedButton("Обнаружить USB", on_click=check_usb),
                file_list,
                ft.Row([
                    ft.ElevatedButton("Назад", on_click=lambda _: page.go("/print"), width=150, height=50),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]
        )
    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
