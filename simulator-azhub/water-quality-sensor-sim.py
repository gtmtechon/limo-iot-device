# 필요한 라이브러리 설치: pip install azure-eventhub
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
import datetime
import random

# Event Hubs 연결 문자열 (Event Hubs 네임스페이스의 공유 액세스 정책에서 'Send' 권한이 있는 연결 문자열)
# 이곳을 실제 디바이스의 연결 문자열로 변경해야 합니다.
# 예시: "HostName=<your-iot-hub>.azure-devices.net;DeviceId=<your-device-id>;SharedAccess
EVENT_HUB_CONNECTION_STR = "Endpoint=sb://limo-evthub-sc01.servicebus.windows.net/;SharedAccessKeyName=acp-evthub-sensor-g1;SharedAccessKey=VgF065j9ZyHUXanxCtGLlZ39rfbdO1X6++AEhMYG9uI=;EntityPath=evthub-sensor-g1"
EVENT_HUB_NAME = "evthub-sensor-g1" # 예: water-quality-data-hub

async def send_water_quality_data():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR,
        eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        while True:
            # 센서 데이터 시뮬레이션
            sensor_data = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "sensor_id": f"sensor-{random.randint(1, 5)}", # 여러 센서 시뮬레이션
                "temperature": round(random.uniform(15.0, 30.0), 2),
                "ph": round(random.uniform(6.5, 8.5), 2),
                "dissolved_oxygen": round(random.uniform(5.0, 12.0), 2),
                #"turbidity": 60
                "turbidity": round(random.uniform(0.5, 50.0), 2)
            }
            event_data = EventData(json.dumps(sensor_data))
            print(f"Sending data: {sensor_data}")
            await producer.send_batch([event_data])
            await asyncio.sleep(5) # 5초마다 데이터 전송

if __name__ == "__main__":
    asyncio.run(send_water_quality_data())