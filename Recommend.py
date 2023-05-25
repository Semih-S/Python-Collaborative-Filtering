import numpy as np
import math

list_for_check = []
file = open("history.txt", "r")
for x in file:
    list_for_check.append(x)

list_for_check = [el.replace('\n', '') for el in list_for_check]
list_for_check.pop(0)
set_for_check = set(list_for_check)
print("Positive Entries:", len(set_for_check))

list_for_avg_angle = []
file = open("history.txt", "r")
for x in file:
    list_for_avg_angle.append(x)

list_for_avg_angle = [el.replace('\n', '') for el in list_for_avg_angle]
Number_of = list_for_avg_angle[0]
list_for_Numbers = [int(x) for x in Number_of.split()]

arrays = []

for i in range(0, list_for_Numbers[1]):
    array = np.zeros((list_for_Numbers[0]))
    arrays.append(array)

transactions = []
for customer_and_item in (list_for_check):
    temp_list = [int(x) for x in customer_and_item.split()]
    transactions.append(temp_list)

transactions = [list(x) for x in set(tuple(x) for x in transactions)]

for transaction in transactions:
    item_y = transaction[1]
    customer_x = transaction[0]
    arrays[item_y - 1][customer_x - 1] += 1


angle_list = []
for i in range(len(arrays)):
    for j in range(i+1, len(arrays)):
        cos_angle = np.dot(
            arrays[i], arrays[j]) / (np.linalg.norm(arrays[i]) * np.linalg.norm(arrays[j]))
        angle = math.degrees(math.acos(cos_angle))
        angle_list.append(angle)

average_angle = np.mean(angle_list)
print(f"Average angle: {average_angle:.2f}")


list_for_queries = []
file2 = open("queries.txt", "r")
for x in file2:
    list_for_queries.append(x)

list_for_queries = [el.replace('\n', '') for el in list_for_queries]

for items in list_for_queries:
    basket = []
    print("Shopping cart:", items)
    itemArr = [int(x) for x in items.split()]
    compare_angle_list = {}
    for item in itemArr:
        basket.append(int(item))
    for index, value in enumerate(arrays):
        if (index + 1) not in basket:
            compare_angle_list[str(index+1)] = value
        else:
            pass

    recommend = []
    for value in basket:
        shortest_angle_list = []
        match_index = 0
        for index, element in compare_angle_list.items():
            recText = ''
            cos_angle = np.dot(element, arrays[value - 1]) / (
                np.linalg.norm(element) * np.linalg.norm(arrays[value - 1]))
            angle = np.arccos(cos_angle)
            angle_degrees = math.degrees(angle)
            if len(shortest_angle_list) > 0:
                prev_smallest_angle = min(shortest_angle_list)
            else:
                prev_smallest_angle = 90.0
            shortest_angle_list.append(angle_degrees)
            curr_smallest_angle = min(shortest_angle_list)
            if prev_smallest_angle > curr_smallest_angle:
                match_index = index

        recommend.append([match_index, curr_smallest_angle])
        recommend.sort(key=lambda x: x[1])
    
        if curr_smallest_angle == 90.0:
            print("Item:", value, "no match")
        else:
            print(
                f"Item: {value}; match: {match_index}; angle: {curr_smallest_angle:.2f}")
    recommend_item = []
    for single_item in recommend:
        if not single_item[0] in recommend_item:
            recommend_item.append(single_item[0])

    print(("Recommend: " + " ".join((recommend_item))).replace(' 0', ''))
