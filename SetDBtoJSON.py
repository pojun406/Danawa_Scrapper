import json
import mariadb

cnx = mariadb.connect(
    user = "root",
    password="root",
    host='localhost',
    port='3306',
    database='pcom'
)
cursor = cnx.cursor()

json_file_paths = [
    'HARDWARE_DATA/Case_List.json',
    'HARDWARE_DATA/Cooler_List.json',
    'HARDWARE_DATA/CPU_List.json',
    'HARDWARE_DATA/HDD_List.json',
    'HARDWARE_DATA/MBoard_List.json',
    'HARDWARE_DATA/Moniter_List.json',
    'HARDWARE_DATA/Power_List.json',
    'HARDWARE_DATA/RAM_List.json',
    'HARDWARE_DATA/SSD_List.json',
    'HARDWARE_DATA/VGA_List.json'
]

for json_file_path in json_file_paths:
    # JSON 파일 열기 및 데이터 읽기
    with open(json_file_path, 'r') as json_file:
        json_data = json_file.read()

    # JSON 데이터 파싱
    data = json.loads(json_data)

    #메뉴팩쳐 = 제조사명
    # saleprice = originalprice의 5% 할인
    # shippingFee는 0으로 고정
    # 쿼니티는 5로 고정
