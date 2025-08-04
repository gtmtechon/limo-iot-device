# 필요한 라이브러리 설치: pip install azure-iot-device
import asyncio
import json
import os
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message # Message 클래스 임포트
from dotenv import load_dotenv

load_dotenv()

# IoT Hub 디바이스 연결 문자열 (Azure Portal에서 디바이스 등록 시 얻은 연결 문자열)
# 이곳을 실제 디바이스의 연결 문자열로 변경해야 합니다.
# 예시: "HostName=<your-iot-hub>.azure-devices.net;DeviceId=<your-device-id>;SharedAccess


# 순차적으로 사용할 위치 좌표 리스트
LOCATIONS = [
    {"latitude": 37.512786, "longitude": 127.106693},
    {"latitude": 37.512276, "longitude": 127.105682},
    {"latitude": 37.511613, "longitude": 127.104878},
    {"latitude": 37.511085, "longitude": 127.103204},
    {"latitude": 37.510421, "longitude": 127.103601},
    {"latitude": 37.510072, "longitude": 127.103837},
    {"latitude": 37.510464, "longitude": 127.105039},
    {"latitude": 37.511136, "longitude": 127.105929},
    {"latitude": 37.511800, "longitude": 127.106701},
    {"latitude": 37.512396, "longitude": 127.107120},
    {"latitude": 37.512685, "longitude": 127.106980}
]

async def main():
    # IoT Hub 클라이언트 생성
    connectionString = os.getenv("R2_IOTHUB_CONNECTION_STRING")
    if not connectionString:
        raise ValueError("IOTHUB_CONNECTION_STRING 환경 변수가 설정되지 않았습니다.")
    print(f"Connecting to IoT Hub with connection string: {connectionString}")
    # IoT Hub 디바이스 클라이언트 생성
    device_client = IoTHubDeviceClient.create_from_connection_string(connectionString) 
    await device_client.connect()
    
    print("Robot connected to IoT Hub.")
    # 위치 리스트를 순환하기 위한 인덱스
    location_index = 0

    # C2D 메시지 수신 핸들러
    async def message_handler(message):
        print(f"===================\n Received C2D message: {message.data.decode('utf-8')}")
        try:
            command_data = json.loads(message.data.decode('utf-8'))
            command = command_data.get("command")
            command_id = command_data.get("command_id")
            parameters = command_data.get("parameters", {})

            print(f"Executing command '{command}' (ID: {command_id}) with parameters: {parameters}")
            # 여기에 실제 로봇 동작 로직 추가
            if command == "adjust_ph_up":
                print(f"Adjusting pH up to {parameters.get('target_ph')}")
            elif command == "activate_filter":
                print(f"Activating filter for {parameters.get('duration_minutes')} minutes")
            # ... 다른 명령 처리

            # 명령 처리 완료 후 IoT Hub에 상태 보고 (선택 사항)
            await send_telemetry({"status": "command_executed", "command_id": command_id, "result": "success"})

        except Exception as e:
            print(f"Error processing C2D message: {e}")
            await send_telemetry({"status": "command_failed", "command_id": command_id, "error": str(e)})

    device_client.on_message_received = message_handler

    # D2C (디바이스-클라우드) 원격 분석 데이터 전송
    async def send_telemetry(data):
        msg_json = json.dumps(data)
        # Message 객체를 생성하고 content_type 및 content_encoding 속성 설정
        msg = Message(msg_json)
        msg.content_type = "application/json"
        msg.content_encoding = "utf-8"
        
        await device_client.send_message(msg)
        print(f"Sent telemetry: {msg_json}") # msg_json을 로그에 출력하여 메시지 내용 확인

    # 주기적으로 로봇 상태 데이터 전송
    while True:
        
        # 현재 위치 가져오기 및 다음 위치 인덱스 업데이트
        current_location = LOCATIONS[location_index]
        location_index = (location_index + 1) % len(LOCATIONS) # 리스트의 끝에 도달하면 처음으로 돌아감


        status_data = {
            "ttimestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "deviceId": "water-purifier-robot-02",
            "type": "robotStatus",
            "batteryLevel": random.randint(10, 90), # 배터리 레벨 10~90% 사이로 랜덤 생성
            "currentStatus": random.choice(["idle", "purifying", "moving"]),
            "purificationStatus": {
                "filterLifeRemaining": random.randint(10, 90),
                "purifiedVolumeLiters": round(random.uniform(100, 500), 2)
            },
            "location": current_location # 순차적으로 변경되는 location 데이터 사용
        }
        await send_telemetry(status_data)
        await asyncio.sleep(10) # 10초마다 상태 전송

if __name__ == "__main__":
    import datetime
    import random
    asyncio.run(main())
