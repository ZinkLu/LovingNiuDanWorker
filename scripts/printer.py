import sys
import tempfile
import time

from utils.logger import logger

if sys.platform == "win32":
    import win32api
    import win32com.client
    import win32print

    def print_file(file_path, printer=None):
        if printer is None:
            logger.info("没有选择打印机，使用默认打印机进行打印")
        printer = printer or win32print.GetDefaultPrinter()
        logger.info("正在使用打印机 {} 打印文件 {}".format(printer, file_path))
        try:
            win32api.ShellExecute(0, "print", file_path, f'/d:"{printer}"', ".", 0)
        except Exception as e:
            logger.info("打印错误，请检查文件")
            logger.exception(e)
            return

    def press_down_enter():
        logger.info("pressing down enter...")
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("{ENTER}")

else:
    logger.warning("No Windows platform found")

    def print_file(file_path, printer=None):
        logger.info("DEBUG: PRINTING...")
        return NotImplemented

    def press_down_enter():
        logger.info("DEBUG: PRESSING...")
        return NotImplemented


def print_pipline(file_path, printer=None, times=2, sleep=3):
    print_file(file_path, printer)
    for _ in range(times):
        time.sleep(sleep)
        press_down_enter()


if __name__ == "__main__":
    filename = tempfile.mktemp(".txt")
    open(filename, "w").write("This is a test")
    print_file(filename)
    press_down_enter()
    time.sleep(3)
    press_down_enter()
