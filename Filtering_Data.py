import codecs
import json

# 제외할 항목
excluded_items = ["HDD (NAS용)", "쿼드로", "고정핀/나사", "VGA 지지대", "써멀패드", "SSD/HDD 주변기기", "임베디드 보드", "방열판", "제온", "중고",
                  "VR 지원 장비", "PowerLink", "SLI Bridge", "노트북", "노트북용", "전용 액세서리", "외장그래픽 독","HDD (기업용)", "HDD (CCTV용)", "DC to DC",
                  "중고 여부 확인요망", "RAM 쿨러", "구매 시 주의사항: 쿨링팬 수(선택), OC(선택), 채굴 여부 판매자 별도 문의 요망", "가이드", "서버용 파워", "서버용",
                  "수랭 부속품", "오일", "인텔(CPU내장)", "조명기기", "채굴용 케이스", "케이블", "튜닝 부속품", "팬 부속품", "팬컨트롤러", "서버용 파워",
                  "제품 상세 정보는 판매중인 쇼핑몰에서 반드시 확인하시기 바랍니다", "DDR2", "방열판 분류용 상품", "메모리, 확장 슬롯, 오디오, 그래픽, USB 출력 별도 확인 요망",
                  "상세스펙 판매처 별도 확인 요망", "UPS", "TFX 파워", "DDR"]
excluded_brands = ["이도디스플레이", "현대파워", "SilverStone", "HALO", "BABEL", "Enhance", "Bestone", "+PLUS", "ANACOMDA"]


json_files = [
    "HARDWARE_DATA_old/Case_List.json",
    "HARDWARE_DATA_old/Cooler_List.json",
    "HARDWARE_DATA_old/CPU_List.json",
    "HARDWARE_DATA_old/HDD_List.json",
    "HARDWARE_DATA_old/MBoard_List.json",
    "HARDWARE_DATA_old/Power_List.json",
    "HARDWARE_DATA_old/RAM_List.json",
    "HARDWARE_DATA_old/SSD_List.json",
    "HARDWARE_DATA_old/VGA_List.json"
]

# JSON 파일들을 읽어서 통합
for file in json_files:
    with codecs.open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)

        # "액세서리" 및 제외할 항목을 포함하지 않는 제품만 추가하고 저장
        filtered_data = [item for item in data if "액세서리" not in item['spec'] and all(excluded_item not in item['spec'] for excluded_item in excluded_items) and "(중고)" not in item['name'] and all(excluded_brand not in item['brand'] for excluded_brand in excluded_brands) and not any("칩:" in spec for spec in item['spec'])and "(콘로)" not in item['name']]

        # 저장할 파일 경로 생성
        save_path = file.replace("HARDWARE_DATA_old/", "HARDWARE_DATA_new/")

        # 필터링된 데이터를 파일로 저장
        with open(save_path, 'w', encoding='utf-8') as save_file:
            json.dump(filtered_data, save_file, ensure_ascii=False, indent=4)
