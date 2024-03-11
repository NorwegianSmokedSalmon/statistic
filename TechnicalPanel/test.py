# a = [1, 2, -1, 3, -1, -1, 5, -1, -1, -1, -1, 6]
# k = 0
# for i in range(len(a)):
#     if a[i - k] == -1:
#         a.remove(-1)
#         k += 1
#
# print(a)

from itertools import groupby

def remove_consecutive_duplicates(lst):
    return [key for key, group in groupby(lst)]

# 测试
numbers = [1, 2, 2, 3, 4, 4, 4, 5, 6, 6, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 5, 3, 3, 3,]
print(remove_consecutive_duplicates(numbers))  # 输出: [1, 2, 3, 4, 5, 6, 7]