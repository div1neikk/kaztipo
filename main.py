import flet as ft

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
                    ft.ElevatedButton("Печать с USB", **button_style),
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

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
