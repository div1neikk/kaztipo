import win32print
import win32ui
import os


class PrinterService:
    """Класс для работы с принтерами и печатью документов"""

    @staticmethod
    def get_printers():
        """Получить список доступных принтеров"""
        return [printer[2] for printer in win32print.EnumPrinters(2)]

    @staticmethod
    def get_default_printer():
        """Получить название принтера по умолчанию"""
        return win32print.GetDefaultPrinter()

    @staticmethod
    def print_document(file_path, copies=1):
        """
        Отправляет документ на печать

        Args:
            file_path (str): Путь к файлу для печати
            copies (int): Количество копий
        """
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