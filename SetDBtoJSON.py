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
    wantCaseSize = product_description.split(";")
    Case_Size = wantCaseSize[0]
    start_index = Case_Size.find("(") + 1
    end_index = Case_Size.find(")")
    Size = Case_Size[start_index:end_index]
    product_img = pc_case.get('img')

    insert_query = "INSERT INTO pc_case(manufacturer_name, product_name, product_salePrice, product_originalPrice, Case_Size, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, Case_Size, product_description, product_img)
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

    Socket = ';'.join(Socket_info)

    print("소켓타입 : ", Socket)



    insert_query = "INSERT INTO pc_cooler(manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket_Type, Color, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket, Color, product_description, product_img)
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

    Socket_Type = product_description[0]

    product_img = pc_cpu.get('img')

    insert_query = "INSERT INTO pc_cpu(manufacturer_name, product_name, product_salePrice, product_originalPrice, TDP, product_description, product_IMG)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, tdp_value, product_description, product_img)
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
    board_size = product_description.split(";")
    Size = board_size[2]
    Socket = board_size[0]

    product_img = pc_mboard.get('img')

    insert_query = "INSERT INTO pc_mboard(manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket, MBoard_Size, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, Socket, Size, product_description, product_img)
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

    split_tmp = product_description.split(";")
    size = pc_ram.get('size')
    print("ram size : " + size)
    Version = split_tmp[1]

    product_img = pc_ram.get('img')

    insert_query = "INSERT INTO pc_ram(manufacturer_name, product_name, product_salePrice, product_originalPrice, R_Size, Version, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, size, Version, product_description, product_img)
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

    product_img = pc_vga.get('img')

    insert_query = "INSERT INTO pc_vga(manufacturer_name, product_name, product_salePrice, product_originalPrice, TDP, Max_Used_W, product_description, product_IMG) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    insert_value = (manufacturer_name, product_name, product_salePrice, product_originalPrice, TDP, Max_Used, product_description, product_img)
    cursor.execute(insert_query, insert_value)

connection.commit()
connection.close()