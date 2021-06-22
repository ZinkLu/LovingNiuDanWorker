import tempfile
import time

import win32api
import win32com.client
import win32print
from utils.logger import logger


def print_file(file_path, printer=None):
    if printer is None:
        logger.info("no printer selected, using default")
    printer = printer or win32print.GetDefaultPrinter()
    logger.info("using print {} to print file {}".format(printer, file_path))
    try:
        win32api.ShellExecute(0, "print", file_path, f'/d:"{printer}"', ".", 0)
    except Exception as e:
        logger.info("print error check log")
        logger.exception(e)
        return


def press_down_enter():
    logger.info("pressing down enter...")
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("{ENTER}")


def print_pipline(file_path, printer=None, times=2, sleep=3):
    print_file(file_path, printer)
    for _ in range(times):
        times.sleep(sleep)
        press_down_enter()


if __name__ == "__main__":
    filename = tempfile.mktemp(".docx")
    open(filename, "w").write("This is a test")
    print_file(filename)
    press_down_enter()
    time.sleep(3)
    press_down_enter()
