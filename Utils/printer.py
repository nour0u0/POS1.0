import os
import json

import win32print
import win32ui
import win32con

from PIL import ImageWin
DM_OUT_BUFFER = 2
DM_IN_BUFFER = 8
DM_FORMNAME = 0x10000

class WindowsPrinter:

    CONFIG_FILE = "PrinterConfig.json"


    def __init__(
        self,
        printer_name=None,
        form_name=None
    ):

        config = self.load_config()


        self.printer_name = (
            printer_name
            or config.get("printer")
            or win32print.GetDefaultPrinter()
        )


        self.form_name = (
            form_name
            or config.get("form")
            or None
        )



    # =====================================
    # CONFIGURATION
    # =====================================


    @classmethod
    def load_config(cls):

        if not os.path.exists(
            cls.CONFIG_FILE
        ):
            return {}


        try:

            with open(
                cls.CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)


        except Exception:

            return {}



    def save_config(self):

        data = {

            "printer": self.printer_name,

            "form": self.form_name

        }


        with open(
            self.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )



    def set_config(
        self,
        printer_name,
        form_name
    ):

        self.printer_name = printer_name

        self.form_name = form_name

        self.save_config()



    # =====================================
    # GET INSTALLED PRINTERS
    # =====================================


    @staticmethod
    def get_printers():

        printers = []


        flags = (
            win32print.PRINTER_ENUM_LOCAL |
            win32print.PRINTER_ENUM_CONNECTIONS
        )


        for printer in win32print.EnumPrinters(flags):

            printers.append(
                printer[2]
            )


        return printers



    # =====================================
    # GET FORMS
    # =====================================


    def get_forms(self):

        handle = win32print.OpenPrinter(
            self.printer_name
        )


        try:

            forms = win32print.EnumForms(
                handle
            )


            return [
                form["Name"]
                for form in forms
            ]


        finally:

            win32print.ClosePrinter(
                handle
            )



    # =====================================
    # APPLY FORM (PLACEHOLDER)
    # =====================================


    


    # =====================================
    # PRINT PIL IMAGE
    # =====================================

    def print_image(self, image):

        dc = None

        try:

            dc = win32ui.CreateDC()

            dc.CreatePrinterDC(
                self.printer_name
            )


            dc.StartDoc(
                "Product Tag"
            )

            dc.StartPage()


            width = dc.GetDeviceCaps(
                win32con.HORZRES
            )

            height = dc.GetDeviceCaps(
                win32con.VERTRES
            )


            dib = ImageWin.Dib(
                image
            )


            dib.draw(
                dc.GetHandleOutput(),
                (
                    0,
                    0,
                    width,
                    height
                )
            )


            dc.EndPage()

            dc.EndDoc()


        except Exception as e:

            raise e


        finally:

            if dc:

                try:
                    dc.DeleteDC()

                except:
                    pass
    def set_form(self):

        if not self.form_name:
            return None


        handle = win32print.OpenPrinter(
            self.printer_name
        )


        try:

            printer_info = win32print.GetPrinter(
                handle,
                2
            )


            devmode = printer_info["pDevMode"]


            # Get current DEVMODE
            win32print.DocumentProperties(
                None,
                handle,
                self.printer_name,
                devmode,
                devmode,
                8 | 2
            )


            # Set paper form
            devmode.FormName = self.form_name


            # DM_FORMNAME flag
            devmode.Fields |= 0x10000


            # Apply changes
            win32print.DocumentProperties(
                None,
                handle,
                self.printer_name,
                devmode,
                devmode,
                8 | 2
            )


            return devmode


        finally:

            win32print.ClosePrinter(
                handle
            )