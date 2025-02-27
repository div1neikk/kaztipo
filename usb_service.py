import os
import psutil
from config import ALLOWED_EXTENSIONS


class USBService:
    """Класс для работы с USB-накопителями"""

    @staticmethod
    def get_usb_drives():
        """Получить список подключенных USB-накопителей"""
        drives = []
        for part in psutil.disk_partitions():
            if "removable" in part.opts or (
                    "cdrom" not in part.opts and part.device.startswith(("/dev/sd", "E:", "F:", "G:"))):
                drives.append(part.device)
        return drives

    @staticmethod
    def list_files_in_usb(drive):
        """
        Получить список файлов на USB-накопителе с поддерживаемыми расширениями

        Args:
            drive (str): Путь к USB-накопителю

        Returns:
            list: Список файлов с поддерживаемыми расширениями
        """
        try:
            return [f for f in os.listdir(drive) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]
        except Exception as e:
            print(f"Ошибка при чтении USB: {str(e)}")
            return []