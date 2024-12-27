from typing import Any, Optional

import psutil
from pynvml import *


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

    def get_vbios_version(self, index: int) -> str:
        handle = self.handle_map[index]
        return nvmlDeviceGetVbiosVersion(handle)

    def get_device_pref(self, index: int) -> str:
        handle = self.handle_map[index]
        return nvmlDeviceGetPerformanceState(handle)

    def get_device_name(self, index: int) -> str:
        handle = self.handle_map[index]
        return nvmlDeviceGetName(handle)

    def get_device_memory_info(self, index: int) -> dict[str, int]:
        handle = self.handle_map[index]
        info = nvmlDeviceGetMemoryInfo(handle)
        return {'total': info.total, 'free': info.free, 'used': info.used}

    def get_device_temperature(self, index: int):
        handle = self.handle_map[index]
        return nvmlDeviceGetTemperature(handle, 0)

    def get_device_fan_speed(self, index: int) -> float:
        handle = self.handle_map[index]
        try:
            return nvmlDeviceGetFanSpeed(handle) * 0.01
        except NVMLError:
            return 0

    def get_compute_processes(self, index: int) -> list[nvmlFriendlyObject]:
        handle = self.handle_map[index]
        return nvmlDeviceGetComputeRunningProcesses(handle)

    def get_device_power_usage(self, index: int) -> int:
        handle = self.handle_map[index]
        return nvmlDeviceGetPowerUsage(handle) * 0.001

    def get_device_power_max(self, index: int) -> int:
        handle = self.handle_map[index]
        try:
            return nvmlDeviceGetPowerManagementLimit(handle) * 0.001
        except NVMLError:
            return 0

    def get_device_utilize(self, index: int):
        handle = self.handle_map[index]
        return nvmlDeviceGetUtilizationRates(handle)
