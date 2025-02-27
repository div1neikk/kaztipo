import flet as ft
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from document_library import DocumentLibrary
from printer_service import PrinterService
from usb_service import USBService
from ui_views import UIViews


def main(page: ft.Page):
    # Инициализация страницы
    page.title = "KazTypo - Система печати"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT

    # Создание сервисов
    printer_service = PrinterService()
    usb_service = USBService()
    doc_library = None

    # Обработчики общих событий
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    def go_back(e):
        page.go("/")

    # Создание менеджера UI представлений
    ui = UIViews(page, go_back, change_theme, usb_service, printer_service)

    # Обработчик для сохранения файла в библиотеку
    def save_to_library(file_path):
        nonlocal doc_library
        if doc_library is None:
            doc_library = DocumentLibrary(page, printer_service.print_document)
        doc_library.add_file_to_library(file_path=file_path)

    # Обработчик изменения маршрута
    def route_change(route):
        nonlocal doc_library
        page.views.clear()

        if page.route == "/":
            page.views.append(ui.main_view())
        elif page.route == "/print":
            page.views.append(ui.print_view())
        elif page.route == "/copy":
            page.views.append(ui.copy_view())
        elif page.route == "/scan":
            page.views.append(ui.scan_view())
        elif page.route == "/price":
            page.views.append(ui.price_view())
        elif page.route == "/advertising":
            page.views.append(ui.advertising_view())
        elif page.route == "/print_usb":
            page.views.append(ui.print_usb_view(
                printer_service.print_document,
                save_to_library
            ))
        elif page.route == "/document_library":
            if doc_library is None:
                doc_library = DocumentLibrary(page, printer_service.print_document)
            page.views.append(doc_library.create_view("/print"))

        page.update()

    # Регистрация обработчика маршрутов
    page.on_route_change = route_change

    # Запуск приложения с начального маршрута
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)