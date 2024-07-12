import requests
from bs4 import BeautifulSoup
import ssl
import csv
import re

def save_to_csv(data, filename):
    # 打开文件准备写入
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        # 创建一个csv写入器
        writer = csv.DictWriter(file, fieldnames=data[0].keys() if data else [])
        # 写入表头（列名）
        writer.writeheader()
        # 写入数据行
        for row in data:
            writer.writerow(row)

def get_able():
    url = 'https://iftp.chinamoney.com.cn/ags/ms/cm-u-bond-md/BondMarketInfoListEN'
    data = {
        "pageNo": "1",
        "pageSize": "15",
        "isin": "",
        "bondCode":"",
        "issueEnty":"",
        "bondType": "100001",
        "couponType":"",
        "issueYear":"2023",
        "rtngShrt":"",
        "bondSpclPrjctVrty":""
    }
    sess = requests.Session()
    sess.keep_alive = False  # 关闭多余连接
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

    response = requests.post(url,data=data, headers=headers, verify=False, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 获取表格
    table =  soup.find('table', class_='san-sheet-alternating')
    rows_data = []
    # 获取表头
    column_names = []
    thead = table.find('thead')
    cells = thead.find_all(['td', 'th'])
    for index, cell in enumerate(cells):
        data_name = cell.get('data-name')
        column_names.append(cell.text.strip())
    rows_data.append(column_names)
    # 表体
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        row_data = {}
        # 遍历该行的每一个单元格
        cells = row.find_all(['td', 'th'])
        for index, cell in enumerate(cells):
            data_name = cell.get('data-name')
            # 将对应的数据添加到字典中，使用列名作为键
            row_data[data_name] = cell.text.strip()
        # 如果字典不为空（即至少有一个我们关心的列的数据），则添加到结果列表中
        if row_data:
            rows_data.append(row_data)
    # 写入csv
    save_to_csv(rows_data, "table.csv")


def reg_search(text, regex_list):

    results = []  # 用于存储所有匹配结果
    for regex in regex_list:
        pattern = re.compile(regex)
        matches = pattern.findall(text)
        if matches:
            results.append(matches)

    return results

if __name__ == '__main__':
    #编程题1
    get_able()
    #编程题2
    reg_search()