import prometheus_client
import uvicorn
from fastapi import FastAPI
from loguru import logger
from prometheus_client import Info, Gauge
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

from nvidia_util import NvidiaReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Define Prometheus metrics
driver_info = Info('nvidia_driver_version', 'NVIDIA driver version')

device_info = Gauge('nvidia_device_info', '', ['device', 'name', 'v_bios', 'p_state'])
gpu_cuda_utilize = Gauge('nvidia_gpu_cuda_utilize', '', ['device'])
gpu_mem_utilize = Gauge('nvidia_gpu_mem_utilize', '', ['device'])
gpu_memory_total = Gauge('nvidia_gpu_memory_total_bytes', 'Total memory of the GPU in bytes', ['device'])
gpu_memory_free = Gauge('nvidia_gpu_memory_free_bytes', 'Free memory of the GPU in bytes', ['device'])
gpu_memory_used = Gauge('nvidia_gpu_memory_used_bytes', 'Used memory of the GPU in bytes', ['device'])
gpu_fan_speed = Gauge('nvidia_gpu_fan_speed_rpm', 'Fan speed of the GPU in RPM', ['device'])
gpu_power_usage = Gauge('nvidia_gpu_power_usage_watts', 'Power usage of the GPU in watts', ['device'])
gpu_power_limit = Gauge('nvidia_gpu_power_limit_watts', 'Power limit of the GPU in watts', ['device'])


@app.get('/metrics')
def get_metrics():
    with NvidiaReader() as reader:
        # Get driver version and set it as a label
        driver_info.info({'version': reader.get_driver_version()})

        # Iterate through all GPUs
        for i in range(reader.device_count):
            device_info.labels(
                device=str(i),
                name=reader.get_device_name(i),
                v_bios=reader.get_vbios_version(i),
                p_state=reader.get_device_pref(i)
            ).set(1)

            utilize = reader.get_device_utilize(i)
            gpu_cuda_utilize.labels(device=f'device {i}').set(utilize.gpu * 0.01)
            gpu_mem_utilize.labels(device=f'device {i}').set(utilize.memory * 0.01)

            # Get memory usage info
            total_memory, free_memory, used_memory = reader.get_device_memory_info(i).items()
            # Update Prometheus metrics
            gpu_memory_total.labels(device=str(i)).set(total_memory[1])
            gpu_memory_free.labels(device=str(i)).set(free_memory[1])
            gpu_memory_used.labels(device=str(i)).set(used_memory[1])

            # Get fan speed and power usage
            fan_speed = reader.get_device_fan_speed(i)
            power_usage = reader.get_device_power_usage(i)
            power_limit = reader.get_device_power_max(i)
            # Update Prometheus metrics for fan speed and power usage
            gpu_fan_speed.labels(device=f'device {i}').set(fan_speed)
            gpu_power_usage.labels(device=f'device {i}').set(power_usage)
            gpu_power_limit.labels(device=f'device {i}').set(power_limit)



    # Return Prometheus metrics
    return Response(
        content=prometheus_client.generate_latest(),
        media_type='text/plain'
    )


def main() -> None:
    uvicorn.run(app, host='0.0.0.0', port=9835)


if __name__ == '__main__':
    main()
