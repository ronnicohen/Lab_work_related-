cage_1 = [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]
cage_2 = [[2, 2], [2, 3], [2, 4], [2, 5]]
cage_3 = [[3, 1], [3, 2], [3, 3], [3, 4], [3, 5]]
cage_4 = [[4, 1], [4, 2], [4, 3], [4, 5]]
cage_5 = [[5, 1], [5, 2], [5, 3], [5, 4], [5, 5]]
cage_6 = [[6, 1], [6, 2], [6, 4]]
all_round1 = [cage_3, cage_5, cage_6]
all_round2 = [cage_1, cage_2, cage_4]
from random import randint


def shuffle_it(allie):
	from copy import deepcopy


	from random import shuffle

	for i in allie:
		shuffle(i)
		shuffle(allie)
	return allie


def randomize(round):
	"""

	:param round:
	:return:[cage, animal, start arm, goal arm, distraction arm]
	"""
	f_start = randint(1,8)
	bob = 0
	n_list = round[0] + round[1] + round[2]
	for i in xrange(0, len(n_list), 2):
		if bob < len(n_list):
			n_list[i].append(f_start)
			goal = f_start + 3
			if goal > 8:
				goal -= 8
			n_list[i].append(goal)
			distraction = f_start + 5
			if distraction > 8:
				distraction -= 8
			n_list[i].append(distraction)
			n_list[i].append(str(f_start) + 'l')
		if i + 1 < len(n_list):
			start2 = f_start - 2
			if start2 < 1:
				start2 = 8 + start2
			n_list[i + 1].append(start2)
			goal = f_start + 3
			if goal > 8:
				goal -= 8
			n_list[i + 1].append(goal)
			n_list[i + 1].append(f_start + 1)
			arena = f_start - 2
			if arena < 1:
				arena += 8
			n_list[i + 1].append(str(arena) + 'r')

		f_start += 3
		bob += 2
		if f_start > 8:
			f_start -= 8
	return round






def print_results(all):
	# what is printed is:
	# [cage number, animal number, start arm, goal arm, distraction arm, arena]
	print 'Animal ----- Start arm ----- goal arm ----- distraction arm ----- ' \
		  'Arena'
	for i in all:
		for j in i:
			print str(j[0]) + '--' + str(j[1]) + '             ' + str(
				j[2]) + '               ' + str(j[
				3]) + '                 ' + str(j[4]) + '               ' + \
				  str(
				j[
					2]) + str(
				j[5])


def write_results(all, name_of_file,how_many_trials):
	import xlwt

	with open(r"C:\Users\ronni\Desktop\%s.csv" % (name_of_file), 'w') as file:
		file.write('Cage, Animal, Start arm, Goal arm, Distraction arm, '
				   'Arena \n')
		for i in xrange(1,int(how_many_trials) +1):
			for i in all:
				for j in i:
					file.write(str(j[0]) + ',' + str(j[1]) + ',' + str(j[2]) + ','
																			   ''
							   + str(j[3]) + ',' + ' ,' +  str(j[5]) + '\n')
					file.write(str(j[0]) + ',' + str(j[1]) + ',' + str(j[2]) + ','
																			   ''
							   + str(j[3]) + ',' + str(j[4]) + ',' + str(j[5]) +
							   '\n')
			file.write(
				'---------------------------------------------------------------\n')


def create_days(num_of_days,num_of_trials):
		num_of_days = int(num_of_days)
		for i in xrange(0, num_of_days):
			shuffled = shuffle_it(all_round1)
			randomized = randomize(shuffled)

			print_results(randomized)
			write_results(randomized, 'RAWM plans day_%s' % (i + 1), num_of_trials)


create_days(5, 3)