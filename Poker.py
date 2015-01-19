"""
Author : RLai
"""

import csv as csv
import numpy as np

def test(data, first_table, second_table):
	suit_table = np.zeros(4)
	rank_table = np.zeros(13)
	hand_table = np.zeros(5)

	for i in range(0,5):
		suit_table[int(data[i*2])-1] += 1
		rank_table[int(data[i*2+1])-1] += 1
		hand_table[i] = int(data[i*2+1]) - 1

	suit_table = list(sorted(suit_table))
	rank_table = sorted(rank_table)
	rank_table = rank_table[8:]
	hand_table = sorted(hand_table)

	first_result = list(suit_table)
	first_result.extend(rank_table)
	first_result.extend(hand_table)

	ans = -1
	check = 0
	for item in first_table:
		if item[0] == first_result :
			ans =  item[1]
			check = 1
			break

	if check == 0 :
		for item in second_table :
			if item[0] == suit_table and item[1] == rank_table :
				ind = max(item[2])
				ans = item[2].index(ind)
				check = 1
				break
			elif item[1] == rank_table : 
				ind = max(item[2])
				ans = item[2].index(ind)
				check  = 1
				break

	return ans

csv_file_object = csv.reader(open('train.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                             # Skip the fist line as it is a header
data=[]                                                     # Create a variable to hold the data

num = 0
for row in csv_file_object:                 # Skip through each row in the csv file
	data.append(row)                        # adding each row to the data variable
	num = num + 1
data = np.array(data)                       # Then convert from a list to an array

print num
suit_table = np.zeros([num, 4])
rank_table = np.zeros([num, 13])
hand_table = np.zeros([num, 5])

for i in range(0, num):
	for j in range(0, 5):
		suit_table[i, int(data[i, j*2])-1] += 1
		rank_table[i, int(data[i, j*2+1])-1] += 1
		hand_table[i, j] = int(data[i, j*2+1])-1

result_table1 = []
result_table2 = []
for i in range(0, num):
	suit_table.sort()
	hand = list(suit_table[i])
	suit = list(hand)
	rank_table.sort()
	rank = list(rank_table[i,8:])
	hand.extend(rank_table[i,8:])
	second = list(hand)
	hand_table.sort()
	hand.extend(hand_table[i])
	first = hand

	index = 0
	for item in result_table1:
		if item[0] == first:
			index = 1
	
	if index == 0:
		result_table1.append([first, int(data[i, 10])])
	
	index = 0
	for item in result_table2:
		if item[0] == suit and item[1] == rank:
			item[2][int(data[i, 10])] += 1
			index = 1
			break
			

	if index == 0:
		ans = [0] * 10
		ans[int(data[i, 10])] = 1
		result_table2.append([suit, rank, ans])
		
csv_file_object = csv.reader(open('test.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                   
data = []

for row in csv_file_object:                 # Skip through each row in the csv file
	data.append(row)                        # adding each row to the data variable

output_file = open("output.csv","wb")
output_file_object = csv.writer(output_file)
output_file_object.writerow(["id","hand"])

for item in data:
	ans = test(item[1:],result_table1,result_table2)
	output_file_object.writerow([int(item[0]), ans])
