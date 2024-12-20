from typing import Any

from pynvml import nvmlInit, nvmlShutdown, nvmlSystemGetDriverVersion, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName


class NvidiaReader:
    def __init__(self):
        nvmlInit()

        self.device_count: int = nvmlDeviceGetCount()
        self.handle_map: dict[int, Any] = {
            i: nvmlDeviceGetHandleByIndex(i)
            for i in range(self.device_count)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        nvmlShutdown()

    def __del__(self):
        nvmlShutdown()

    @staticmethod
    def get_driver_version() -> str:
        return nvmlSystemGetDriverVersion()

    def get_device_name(self, index: int) -> str:
        handle = self.handle_map[index]
        return nvmlDeviceGetName(handle)
