# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    # print(len(cities), len(set(cities)))

    # 获取坐标文件中所有地名
    data = None
    with open(
            '/Users/wangbo/PycharmProjects/python-spider/venv/lib/python3.6/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                # print(k, city)
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(
            '/Users/wangbo/PycharmProjects/python-spider/venv/lib/python3.6/site-packages/pyecharts/datasets/city_coordinates.json',
            mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

