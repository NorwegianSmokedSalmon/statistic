# 打开并读取文件
with open('data.txt', 'r') as file:
    lines = file.readlines()

# 初始化一个空列表来存储所有的列表
data_lists = []

# 遍历文件中的每一行
for line in lines:
    # 使用eval函数将字符串转换为列表
    data_list = eval(line.strip())
    # 将列表添加到大列表中
    data_lists.append(data_list)

for data_list in data_lists:
    print(data_list)