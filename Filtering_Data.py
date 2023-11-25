import codecs
import json
import subprocess

subprocess.run(["python", "Case.py"])
subprocess.run(["python", "Cooler.py"])
subprocess.run(["python", "CPU.py"])
subprocess.run(["python", "HDD.py"])
subprocess.run(["python", "MBoard.py"])
subprocess.run(["python", "Power.py"])
subprocess.run(["python", "RAM.py"])
subprocess.run(["python", "SSD.py"])
subprocess.run(["python", "VGA.py"])

# 제외할 항목
excluded_items = ["HDD (NAS용)", "쿼드로", "고정핀/나사", "VGA 지지대", "써멀패드", "SSD/HDD 주변기기", "임베디드 보드", "방열판", "제온", "중고",
                  "VR 지원 장비", "PowerLink", "SLI Bridge", "노트북", "노트북용", "전용 액세서리", "외장그래픽 독","HDD (기업용)", "HDD (CCTV용)", "DC to DC", "HDD (노트북용)",
                  "중고 여부 확인요망", "RAM 쿨러", "구매 시 주의사항: 쿨링팬 수(선택), OC(선택), 채굴 여부 판매자 별도 문의 요망", "가이드", "서버용 파워", "서버용",
                  "수랭 부속품", "오일", "인텔(CPU내장)", "조명기기", "채굴용 케이스", "케이블", "튜닝 부속품", "팬 부속품", "팬컨트롤러", "서버용 파워",
                  "제품 상세 정보는 판매중인 쇼핑몰에서 반드시 확인하시기 바랍니다", "DDR2", "방열판 분류용 상품", "메모리, 확장 슬롯, 오디오, 그래픽, USB 출력 별도 확인 요망",
                  "상세스펙 판매처 별도 확인 요망", "UPS", "TFX 파워", "DDR", "시스템 쿨러", "VGA 쿨러", "M.2 SSD 쿨러", "써멀 컴파운드", "먼지필터", "USB헤더 허브", "더미램",
                  "HDD 쿨러", "HDD (리퍼비시)", "SSHD (노트북용)", "SSHD (PC용)", "튜닝 케이스", "랙마운트", "H300~H750 허브랙 전용", "HTPC 케이스", "브라켓/가이드", "전원부: 18+1+2페이즈",
                  "메모리 DDR4 노트북용", "인텔 B250", "인텔 C252", "PC케이스(RTX)", "라이저 케이블", "일반-ATX (30.5 x 22.5cm)", "M-DTX (20.3x17.0cm)", "LGA1155", "메모리 규격: DDR3",
                  "메모리 규격: DDR3, DDR2", "메모리 규격: DDR2", "커버/먼지필터", "써멀 페이스트 가드"]
excluded_brands = ["셀텍", "모드컴", "be", "이도디스플레이", "현대파워", "SilverStone", "HALO", "BABEL", "Enhance", "Bestone", "+PLUS", "ANACOMDA", "FOXCONN", "EVERCOOL", "NOCTUA"]
excluded_sockets = ["AMD(소켓TR4)", "AMD(소켓SP3)", "AMD(소켓sTRX4)", "인텔(소켓775)", "인텔(소켓2011)", "LGA2011", "LGA2011-V3", "LGA 1366", "인텔(소켓1155)", "소켓2011-V3", "소켓 sTRX4", "소켓 TR4", "소켓1151v2", "소켓sWRX8", "AMD(소켓SP5)", "인텔(소켓4677)", "인텔(소켓4189)", "인텔(소켓3647)", "인텔(소켓2066)", "산업용SSD", "GDDR2(DDR2)", "외장그래픽", "노트북", "DDR2", "DDR3"]

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
        filtered_data = [item for item in data if "액세서리" not in item['spec']
                         and all(excluded_item not in item['spec'] for excluded_item in excluded_items)
                         and "(중고)" not in item['name']
                         and "중고" not in item['name']
                         and "해외구매" not in item['name']
                         and "병행수입" not in item['name']
                         and all(excluded_brand not in item['brand'] for excluded_brand in excluded_brands)
                         and not any("칩:" in spec for spec in item['spec'])
                         and "(콘로)" not in item['name']
                         and "일시품절" not in item['price']
                         and "가격비교예정" not in item['price']
                         and not any(word in ''.join(item.get('spec', [])) for word in excluded_sockets)]

        # 저장할 파일 경로 생성
        save_path = file.replace("HARDWARE_DATA_old/", "HARDWARE_DATA_new/")

        if "Case_List" in file and any("GPU 장착:" in item['spec'] for item in data):
            filtered_data += [item for item in data if "GPU 장착:" in item['spec']]

        # 필터링된 데이터를 파일로 저장
        with open(save_path, 'w', encoding='utf-8') as save_file:
            json.dump(filtered_data, save_file, ensure_ascii=False, indent=4)
