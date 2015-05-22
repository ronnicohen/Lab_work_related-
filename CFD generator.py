"""
This script creates an excel file containing 8 days of contextual fear
discrimination settings, complete with chamber assignment, shuffling of cages
and of the animals within the cages, reversal of the chambers for the second
run each day.
Most crucially, it organizes the shuffled order so that the two
chambers will be used at all time (if the number of animals is even),
thus saving experimental run time.

The output file contains a different sheet for each day, and might need to be
touched up esthetically as it is by default very bare.
"""



# The list of cages is taken from other scripts for the same animals.
# each cage contains lists representing each animal, this list is:
# [number of cage , number of animal, irrelevant number from previous work]
cage_1 = [[1, 1, 2], [1, 2, 2], [1, 3, 4], [1, 4, 3], [1, 5, 2]]
cage_2 = [[2, 2, 2], [2, 3, 3], [2, 4, 4], [2, 5, 1]]
cage_3 = [[3, 1, 4], [3, 2, 1], [3, 3, 2], [3, 4, 3], [3, 5, 1]]
cage_4 = [[4, 1, 3], [4, 2, 2], [4, 3, 2], [4, 5, 1]]
cage_5 = [[5, 1, 1], [5, 2, 3], [5, 3, 4], [5, 4, 1], [5, 5, 1]]
cage_6 = [[6, 1, 4], [6, 2, 3], [6, 4, 4]]
all = [cage_1, cage_2, cage_3, cage_4, cage_5, cage_6]
from copy import deepcopy


def make_one_list():
	"""
	Makes the list of lists into a single list, all animals of the same cage
	remain together
	:return: a single list of lists
	"""
	new_list = []
	for i in all:
		for j in i:
			new_list.append(j)
	return new_list


def assign_chamber():
	"""
	takes the output of make_one_list and appends chamber 'A' to half the
	animals and chamber 'B' to the other half.
	If the number of animals in a cage is even, there will be an equal amount
	of both conditions in it
	"""
	merged_list = make_one_list()
	curr = 1
	for i in merged_list:
		if curr % 2 == 0:
			i.append('A')
		else:
			i.append('B')
		curr += 1


def shuffle_and_mix():
	"""
	This function simply shuffles the animals in each cage and the cages
	:return:
	"""
	from random import shuffle
	for i in all:
		shuffle(i)
	shuffle(all)
	return all


def make_duos(alli):
	"""
	This function runs over the order of randomized animals and checks that
	both chambers are used. If they are not, it will change the order in the
	cage (or the following cage, if needed [this can be done once per cage])
	so that  both chambers will be in use at all times
	:param alli:
	:return:
	"""
	skip = False
	for i in xrange(0, len(alli)):
		if skip is False:
			for j in xrange(0, len(alli[i]), 2):
				if j + 1 <= len(alli[i]) - 1:
					if not (alli[i][j][3] != alli[i][j + 1][3]):
						for k in xrange(j + 1, len(alli[i])):
							if k <= len(all[i]):
								if alli[i][j][3] != alli[i][k][3]:
									holder = deepcopy((alli[i][k]))
									alli[i][k] = deepcopy(alli[i][j + 1])
									alli[i][j + 1] = deepcopy(holder)
									skip = False
									break
					else:
						skip = False
				else:
					if i + 1 <= len(alli) - 1:
						for k in xrange(0, len(alli[i + 1])):
							if alli[i][j][3] != alli[i + 1][k][3]:
								holder = deepcopy((alli[i + 1][0]))
								alli[i + 1][0] = deepcopy(alli[i + 1][k])
								alli[i + 1][k] = holder
								skip = True
								break
		else:
			for j in xrange(1, len(alli[i]), 2):
				if j + 1 <= len(alli[i]) - 1:
					if not (alli[i][j][3] != alli[i][j + 1][3]):
						for k in xrange(j + 1, len(alli[i])):
							if k <= len(all[i]):
								if alli[i][j][3] != alli[i][k][3]:
									holder = deepcopy((alli[i][k]))
									alli[i][k] = deepcopy(alli[i][j + 1])
									alli[i][j + 1] = deepcopy(holder)
									skip = False
									break
					else:
						skip = False
				else:
					if i + 1 <= len(alli) - 1:
						for k in xrange(0, len(alli[i + 1])):
							if alli[i][j][3] != alli[i + 1][k][3]:
								holder = deepcopy((alli[i + 1][0]))
								alli[i + 1][0] = deepcopy(alli[i + 1][k])
								alli[i + 1][k] = holder
								skip = True
								break
	return alli


def main():
	"""
	This function calls al the others in order and assigns the amount of days
	"""
	assign_chamber()
	biggie = []
	for i in xrange(0, 8):
		shuffled = shuffle_and_mix()
		organized = make_duos(shuffled)
		biggie.append(deepcopy(organized))
	write_to_excel(biggie)


def write_to_excel(biggie):
	"""
	This function accepts the finished list of animals and writes them to the
	excel workbook.
	:param biggie: the finished list
	"""
	import xlwt
	workbook = xlwt.Workbook()
	day_1 = workbook.add_sheet('day_1')
	write_worksheets(day_1, biggie, 1)
	day_2 = workbook.add_sheet('day_2')
	write_worksheets(day_2, biggie, 2)
	day_3 = workbook.add_sheet('day_3')
	write_worksheets(day_3, biggie, 3)
	day_4 = workbook.add_sheet('day_4')
	write_worksheets(day_4, biggie, 4)
	day_5 = workbook.add_sheet('day_5')
	write_worksheets(day_5, biggie, 5)
	day_6 = workbook.add_sheet('day_6')
	write_worksheets(day_6, biggie, 6)
	day_7 = workbook.add_sheet('day_7')
	write_worksheets(day_7, biggie, 7)
	day_8 = workbook.add_sheet('day_8')
	write_worksheets(day_8, biggie, 8)
	workbook.save(r"C:\Users\ronni\Desktop\test\exp. CFD 8 days.xls")


def write_worksheets(sheet, biggie, day):
	"""
	This function fills a specific sheet with the appropriate information
	from the finished list
	:param sheet: the sheet to be worked on
	:param biggie: the finished list of animals, cages, conditions and order
	:param day: the number of test day
	"""
	sheet.write(0, 0, 'exp. CFD')
	sheet.write(2, 1, 'Day: ')
	sheet.write(2, 2, day)
	sheet.write(3, 1, 'Date: ')
	sheet.write(5, 1, 'Cage')
	sheet.write(5, 2, 'Animal')
	sheet.write(5, 3, 'Chamber')
	sheet.write(5, 4, 'Done')
	cages = []
	animals = []
	chambers = []
	reversed_chambers = []
	smalls = reverse_chambers(biggie)
	for i in biggie[day - 1]:
		for j in i:
			cages.append(j[0])
			animals.append(j[1])
			chambers.append(j[3])
	for i in smalls[day - 1]:
		for j in i:
			reversed_chambers.append(j[3])
	for i in xrange(0, len(cages)):
		sheet.write(i + 6, 1, cages[i])
		sheet.write(i + 6, 2, animals[i])
		sheet.write(i + 6, 3, chambers[i])
	sheet.write(len(cages) + 6, 0, '--------')

	for i in xrange(len(cages) + 1, (2 * len(cages)) + 1):
		sheet.write(i + 6, 1, cages[i - (len(cages) + 1)])
		sheet.write(i + 6, 2, animals[i - (len(cages) + 1)])
		sheet.write(i + 6, 3, reversed_chambers[i - (len(cages) + 1)])


def reverse_chambers(biggie):
	"""
	this function changes the conditions for all animals, which is required
	for the second half of the trial
	:param biggie:
	:return:
	"""
	smalls = deepcopy(biggie)
	for i in smalls:
		for j in i:
			for k in j:
				if k[3] == 'A':
					k[3] = 'B'
				else:
					k[3] = 'A'
	return smalls


main()

