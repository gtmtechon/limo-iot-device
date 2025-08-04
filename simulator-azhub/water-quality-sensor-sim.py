# 필요한 라이브러리 설치: pip install azure-eventhub
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Event Hubs 연결 문자열 (Event Hubs 네임스페이스의 공유 액세스 정책에서 'Send' 권한이 있는 연결 문자열)
# 이곳을 실제 디바이스의 연결 문자열로 변경해야 합니다.

async def send_water_quality_data():
    
    connectionString = os.getenv("EVENTHUB_CONNECTION_STRING")
    if not connectionString:
        raise ValueError("EVENTHUB_CONNECTION_STRING 환경 변수가 설정되지 않았습니다.")
    print(f"EVENTHUB_CONNECTION_STRING: {connectionString}")
    
    eventhubName =os.getenv("EVENT_HUB_NAME")
    if not eventhubName:
       raise ValueError("EVENT_HUB_NAME 환경 변수가 설정되지 않았습니다.")
    print(f"EVENT_HUB_NAME: {eventhubName}")
 
    
    consumerGroupName = os.getenv("EVENT_HUB_CONSUMER_GROUP_NAME")
    if not consumerGroupName:
        raise ValueError("EVENTHUB_CONSUMNER_GROUP_NAME 환경 변수가 설정되지 않았습니다.")
    print(f"EVENT_HUB_CONSUMER_GROUP_NAME: {consumerGroupName}")
    
    
    
    # 사용자가 제공한 센서 ID 목록
    sensor_ids = [
        "PPZof7g2BwfipKVU",
        "oltD2DuyGZONFf2k",
        "QUDAFUIEMGX8U3NY",
        "XEuLO75SS3nElEy6",
        "xWjzBRdluhWw4Vj8"
    ]
    
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connectionString,
        eventhub_name=eventhubName,
        consumer_group=consumerGroupName
    )
    async with producer:
        while True:
            # 센서 데이터 시뮬레이션
            selected_sensor_id = random.choice(sensor_ids) # 랜덤 센서 ID 선택
            sensor_data = {
                "ttimestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "type": "lakeStatus",
                "sensorId": selected_sensor_id, # 제공된 목록에서 랜덤 선택
                "temperature": round(random.uniform(15.0, 30.0), 2),
                "ph": round(random.uniform(6.5, 8.5), 2),
                "dissolvedOxygen": round(random.uniform(5.0, 12.0), 2),
                "turbidity": round(random.uniform(0.5, 50.0), 2)
            }
            event_data = EventData(json.dumps(sensor_data))
            print(f"Sending data for sensor {selected_sensor_id} with partition key {selected_sensor_id}: {sensor_data}")
            await producer.send_batch([event_data], partition_key=selected_sensor_id) # partition_key를 send_batch에 전달
            await asyncio.sleep(10) # 5초마다 데이터 전송

if __name__ == "__main__":
    asyncio.run(send_water_quality_data())
