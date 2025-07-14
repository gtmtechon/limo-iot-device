# limo-iot-device


## message spec.
###  디바이스-클라우드 (D2C) 메시지 규격 (로봇 -> IoT Hub). 
{
  "timestamp": "2025-07-10T14:30:00.123Z",  
  "device_id": "water-purifier-robot-01",  
  "battery_level": 85,        // 배터리 잔량 (%). 
  "current_status": "idle",   // idle, moving, purifying, charging, error. 
  "last_command_id": "cmd-12345", // 마지막으로 수신한 명령 ID (선택 사항). 
  "purification_status": {    // 정화 작업 관련 데이터 (작업 중일 때만 포함). 
    "filter_life_remaining": 70, // 필터 잔량 (%). 
    "purified_volume_liters": 150 // 정화된 총량 (리터). 
  },  
  "location": {               // 현재 위치 (선택 사항). 
    "latitude": 37.5665,  
    "longitude": 126.9780. 
  },  
  "error_code": null          // 에러 발생 시 코드 (예: "E001: Filter Clogged"). 
}. 


### 클라우드-디바이스 (C2D) 메시지 규격 (IoT Hub -> 로봇)
{
  "command_id": "cmd-67890",      // 명령의 고유 ID
  "command": "adjust_ph_up",      // 수행할 명령 (예: adjust_ph_up, adjust_ph_down, activate_filter, move_to_location, return_to_base)
  "parameters": {                 // 명령에 필요한 매개변수
    "target_ph": 7.0,
    "reason": "Low pH detected",
    "duration_minutes": null,
    "latitude": null,
    "longitude": null
  },
  "issued_at": "2025-07-10T14:31:00.000Z"
}