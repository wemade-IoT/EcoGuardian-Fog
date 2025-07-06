from typing import Optional
from iam.domain.entities import Device

_devices_memory = {}

class DeviceRepository:
    @staticmethod
    def find_by_id_and_api_key(device_id: int, api_key: str):
        device = _devices_memory.get(device_id)
        if device and device.api_key == api_key:
            return device
        return None

    @staticmethod
    def get_or_create_test_device(device_id: int, api_key: str) -> Optional[Device]:
        from datetime import datetime
        if device_id not in _devices_memory:
            from iam.domain.entities import Device
            device = Device(device_id, api_key, datetime.now())
            _devices_memory[device_id] = device
            return device
        return _devices_memory[device_id]
