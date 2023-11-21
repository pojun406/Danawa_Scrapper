import json
import mysql.connector
import re

# MariaDB 연결 정보
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'pcom'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

with open('HARDWARE_DATA_new/Case_List.json', 'r', encoding='utf-8') as f:
    case_data = json.load(f)
with open('HARDWARE_DATA_new/Cooler_List.json', 'r', encoding='utf-8') as f:
    cooler_data = json.load(f)
with open('HARDWARE_DATA_new/CPU_List.json', 'r', encoding='utf-8') as f:
    cpu_data = json.load(f)
with open('HARDWARE_DATA_new/HDD_List.json', 'r', encoding='utf-8') as f:
    hdd_data = json.load(f)
with open('HARDWARE_DATA_new/MBoard_List.json', 'r', encoding='utf-8') as f:
    mboard_data = json.load(f)
with open('HARDWARE_DATA_new/power_List.json', 'r', encoding='utf-8') as f:
    power_data = json.load(f)
with open('HARDWARE_DATA_new/RAM_List.json', 'r', encoding='utf-8') as f:
    ram_data = json.load(f)
with open('HARDWARE_DATA_new/SSD_List.json', 'r', encoding='utf-8') as f:
    ssd_data = json.load(f)
with open('HARDWARE_DATA_new/VGA_List.json', 'r', encoding='utf-8') as f:
    vga_data = json.load(f)

delete_query1 = "DELETE FROM pc_case"
delete_query2 = "DELETE FROM pc_cooler"
delete_query3 = "DELETE FROM pc_cpu"
delete_query4 = "DELETE FROM pc_hdd"
delete_query5 = "DELETE FROM pc_mboard"
delete_query6 = "DELETE FROM pc_power"
delete_query7 = "DELETE FROM pc_ram"
delete_query8 = "DELETE FROM pc_ssd"
delete_query9 = "DELETE FROM pc_vga"

cursor.execute(delete_query1)
cursor.execute(delete_query2)
cursor.execute(delete_query3)
cursor.execute(delete_query4)
cursor.execute(delete_query5)
cursor.execute(delete_query6)
cursor.execute(delete_query7)
cursor.execute(delete_query8)
cursor.execute(delete_query9)

alter_query = "ALTER TABLE pc_case AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_cooler AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_cpu AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_hdd AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_mboard AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_power AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_ram AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_ssd AUTO_INCREMENT = 1"
cursor.execute(alter_query)
alter_query = "ALTER TABLE pc_vga AUTO_INCREMENT = 1"
cursor.execute(alter_query)
insert_default_cooler = "INSERT INTO pc_cooler (product_num, manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket_Type, Color, product_description, product_IMG) VALUES (0, '기본쿨러', '기본쿨러', '0', '0', NULL, NULL, NULL, NULL)"
cursor.execute(insert_default_cooler)

for pc_case in case_data:
    manufacturer_name = pc_case.get('brand')
    product_name = pc_case.get('name')
    product_price = pc_case.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_case.get('spec'))
    Size = pc_case.get('spec')[0]
    Color = pc_case.get('color_text')
    matches = re.search(r'\(([^)]+)\)', Size)
    if matches:
        C_Size = matches.group(1)
    else:
        C_Size = Size

    match_gpu1 = re.search(r'GPU 장착: (?:최대 )?(\d+)mm', product_description)
    match_gpu2 = re.search(r'GPU 장착: (\d+)~(\d+)mm', product_description)
    if match_gpu1:
        gpu_size = match_gpu1.group(1)
    elif match_gpu2:
        gpu_size = match_gpu2.group(2)
    else:
        gpu_size = 0


    #start_index = Case_Size.find("(") + 1
    #end_index = Case_Size.find(")")
    #Size = Case_Size[start_index:end_index]
    product_img = pc_case.get('img')
    if gpu_size != 0:
        insert_query = "INSERT INTO pc_case(manufacturer_name, product_name, product_salePrice, product_originalPrice, Board_Size, GPU_Size, Color, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, C_Size, gpu_size, Color, product_description, product_img)
        cursor.execute(insert_query, insert_value)


for pc_cpu in cpu_data:
    manufacturer_name = pc_cpu.get('brand')
    product_name = pc_cpu.get('name')
    product_price = pc_cpu.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_cpu.get('spec'))
    tdp_one = r'TDP: (\d+)W'
    tdp_wave = r'TDP: (\d+)~(\d+)W'
    PBP_one = r'PBP/MTP: (\d+)W'
    PBP_wave = r'PBP/MTP: (\d+)~(\d+)W'
    matches1 = re.search(tdp_one, product_description)
    if matches1:
        tdp_value = matches1.group(1)
    else:
        matches2 = re.search(tdp_wave, product_description)
        if matches2:
            tdp_value = matches2.group(2)
        else:
            matches3 = re.search(PBP_one, product_description)
            if matches3:
                tdp_value = matches3.group(1)
            else:
                matches4 = re.search(PBP_wave, product_description)
                if matches4:
                    tdp_value = matches4.group(2)
                else:
                    tdp_value = 0

    socket_info = pc_cpu.get('spec')[0]
    WhatSocket = list(socket_info)
    formatted_socket_info = ""

    matches = re.search(r'내장그래픽: (\S+);', product_description)
    if matches:
        integrated_graphics = matches.group(1)

    matches_mem = re.search(r'메모리 규격: ((?:DDR[0-9]+,? ?)+)', product_description)
    if matches_mem:
        memory_type = matches_mem.group(1).strip()

    if WhatSocket[0] == "인":
        matches1 = re.search(r'인텔\(소켓(\d+)\)', socket_info)
        if matches1:
            socket_number = matches1.group(1)
            formatted_socket_info = f"LGA{socket_number}"
    elif WhatSocket[0] == "A":
        matches2 = re.search(r'AMD\(소켓([A-Za-z0-9]+)\)', socket_info)
        if matches2:
            socket_number = matches2.group(1)
            formatted_socket_info = f"{socket_number}"
    product_img = pc_cpu.get('img')

    def_cooler = re.search(r'쿨러: (.+?);', product_description)
    if def_cooler:
        cooler_stat = def_cooler.group(1)

    insert_query = "INSERT INTO pc_cpu(manufacturer_name, product_name, product_salePrice, product_originalPrice, InterGrated_graphics, TDP, Socket_Type, Memory_Type, Stock_Cooler, product_description, product_IMG)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, integrated_graphics, tdp_value, formatted_socket_info, memory_type, cooler_stat, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_cooler in cooler_data:
    manufacturer_name = pc_cooler.get('brand')
    product_name = pc_cooler.get('name')
    product_price = pc_cooler.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_cooler.get('spec'))
    Color = pc_cooler.get("color_text")
    product_img = pc_cooler.get('img')

    Socket_Type = []
    for keyword in pc_cooler.get('spec'):
        if '소켓:' in keyword:
            Socket_Type.append(keyword)

    Socket_info = []
    for item in Socket_Type:
    # "인텔 소켓:" 뒤에 있는 정보 추출
        intel_sockets = re.search(r'인텔 소켓: (.+)', item)
        if intel_sockets:
            Socket_info.extend(intel_sockets.group(1).split(', '))

        # "AMD 소켓:" 뒤에 있는 정보 추출
        amd_sockets = re.search(r'AMD 소켓: (.+)', item)
        if amd_sockets:
            Socket_info.extend(amd_sockets.group(1).split(', '))

    Socket = ','.join(Socket_info)

    print("소켓타입 : " + Socket)



    insert_query = "INSERT INTO pc_cooler(manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket_Type, Color, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket, Color, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_hdd in hdd_data:
    manufacturer_name = pc_hdd.get('brand')
    product_name = pc_hdd.get('name')
    product_price = pc_hdd.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_hdd.get('spec'))
    hdd_size = ''.join(pc_hdd.get('size'))

    product_img = pc_hdd.get('img')

    insert_query = "INSERT INTO pc_hdd(manufacturer_name, product_name, product_salePrice, product_originalPrice, D_Size, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, hdd_size, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_mboard in mboard_data:
    manufacturer_name = pc_mboard.get('brand')
    product_name = pc_mboard.get('name')
    product_price = pc_mboard.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_mboard.get('spec'))
    Size = pc_mboard.get('spec')[2]
    pattern = r'\([^)]*\)'
    result = re.sub(pattern, '', Size)
    M_Size = result.strip()

    Socket = pc_mboard.get('spec')[0]
    WhatSocket = list(Socket)
    formatted_socket_info = ""

    if WhatSocket[0] == "인":
        matches1 = re.search(r'인텔\(소켓(\d+)\)', Socket)
        if matches1:
            socket_number = matches1.group(1)
            formatted_socket_info = f"LGA{socket_number}"
    elif WhatSocket[0] == "A":
        matches2 = re.search(r'AMD\(소켓([A-Za-z0-9]+)\)', Socket)
        if matches2:
            socket_number = matches2.group(1)
            formatted_socket_info = f"{socket_number}"

    get_Memory = r'\b메모리\s+(DDR[0-9]+)\b'
    Memory_match = re.search(get_Memory, product_description)
    if Memory_match:
        memory_type = Memory_match.group(1)
        print(memory_type)

    MHzType = product_description
    getMHz = r'(;\d{1,4}(?:,\d{3})*MHz)'
    MHz_match = re.search(getMHz, MHzType)

    product_img = pc_mboard.get('img')
    MHz = 0
    if MHz_match:
        MHz_raw = ''.join(re.findall(r'\d', MHz_match.group())).replace(',', '')  # "3200MHz"에서 "3200"을 가져옴
        MHz = int(MHz_raw)

    if MHz != "":
        insert_query = "INSERT INTO pc_mboard(manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket, Memory_Type, MHz, MBoard_Size, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, formatted_socket_info, memory_type, MHz, M_Size, product_description, product_img)
        cursor.execute(insert_query, insert_value)

for pc_power in power_data:
    manufacturer_name = pc_power.get('brand')
    product_name = pc_power.get('name')
    product_price = pc_power.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_power.get('spec'))
    board_size = product_description.split(";");
    Watt = board_size[1]
    W = re.findall(r'\d+', Watt)
    W_str = ''.join(W)


    product_img = pc_power.get('img')


    insert_query = "INSERT INTO pc_power(manufacturer_name, product_name, product_salePrice, product_originalPrice, W, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, W_str, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_ram in ram_data:
    manufacturer_name = pc_ram.get('brand')
    product_name = pc_ram.get('name')
    product_price = pc_ram.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95


    product_description = ';'.join(pc_ram.get('spec'))

    size = pc_ram.get('size')
    Version = pc_ram.get('spec')[1]
    ram_type = pc_ram.get('spec')[2]
    getMHz = r'(\d+MHz)'
    matchs = re.search(getMHz, ram_type)
    if matchs:
        MHz_raw = matchs.group(1)
        MHz = int(re.search(r'\d+', MHz_raw).group())

    product_img = pc_ram.get('img')

    insert_query = "INSERT INTO pc_ram(manufacturer_name, product_name, product_salePrice, product_originalPrice, R_Size, Version, MHz, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, size, Version, MHz, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_ssd in ssd_data:
    manufacturer_name = pc_ssd.get('brand')
    product_name = pc_ssd.get('name')
    product_price = pc_ssd.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_ssd.get('spec'))
    ssd_size = ''.join(pc_ssd.get('size'))

    product_img = pc_ssd.get('img')

    insert_query = "INSERT INTO pc_ssd(manufacturer_name, product_name, product_salePrice, product_originalPrice, S_Size, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, ssd_size, product_description, product_img)
    cursor.execute(insert_query, insert_value)

for pc_vga in vga_data:
    manufacturer_name = pc_vga.get('brand')
    product_name = pc_vga.get('name')
    product_price = pc_vga.get('price')

    if product_price == '일시품절':
        product_originalPrice = '일시품절'
        product_salePrice = 0  # '일시품절'인 경우 0으로 할당
    elif product_price == '가격비교예정':
        product_originalPrice = '가격비교예정'
        product_salePrice = 0  # '가격비교예정'인 경우 0으로 할당
    else:
        product_originalPrice = product_price
        product_salePrice = int(product_price) * 0.95

    product_description = ';'.join(pc_vga.get('spec'))
    useW = r'사용전력: (\d+)W'
    max_useW = r'사용전력: 최대 (\d+)W'
    matches = re.search(useW, product_description)
    if matches:
        TDP = matches.group(1)
    else:
        matches_max = re.search(max_useW, product_description)
        if matches_max:
            TDP = matches_max.group(1)
        else:
            TDP = 0

    maxW = r'정격파워 (\d+)W'
    matches2 = re.search(maxW, product_description)
    if matches2:
        Max_Used = matches2.group(1)
        print("최대 사용 와트 : " + Max_Used)
    else:
        Max_Used = 0

    match_length = re.search(r'가로\(길이\): (\d+(\.\d+)?)mm', product_description)
    if match_length:
        VGA_size = match_length.group(1)
    else:
        VGA_size = 0

    VGA_Name = pc_vga.get('spec')[0]
    product_img = pc_vga.get('img')
    if TDP != 0 or Max_Used != 0:
        insert_query = "INSERT INTO pc_vga(manufacturer_name, product_name, product_salePrice, product_originalPrice, VGA_Name, VGA_Size, TDP, Max_Used_W, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, VGA_Name, VGA_size, TDP, Max_Used, product_description, product_img)
        cursor.execute(insert_query, insert_value)

connection.commit()
connection.close()