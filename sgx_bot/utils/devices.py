# (c) 2021 KassemSYR || SamsungGeeksBot

from requests import get
from ujson import loads


class GetDevice:
    def __init__(self, device):
        """Get device info by codename or model!"""
        self.device = device

    def get(self):
        if self.device.lower().startswith("sm-"):
            data = get(
                "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_model.json"
            ).content
            db = loads(data)
            try:
                name = db[self.device.upper()][0]["name"]
                device = db[self.device.upper()][0]["device"]
                brand = db[self.device.upper()][0]["brand"]
                model = self.device.lower()
                return {"name": name, "device": device, "model": model, "brand": brand}
            except KeyError:
                return False
        else:
            data = get(
                "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"
            ).content
            db = loads(data)
            newdevice = (
                self.device.strip("lte").lower()
                if self.device.startswith("beyond")
                else self.device.lower()
            )
            try:
                name = db[newdevice][0]["name"]
                model = db[newdevice][0]["model"]
                brand = db[newdevice][0]["brand"]
                device = self.device.lower()
                return {"name": name, "device": device, "model": model, "brand": brand}
            except KeyError:
                return False
