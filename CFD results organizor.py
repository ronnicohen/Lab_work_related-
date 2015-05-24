"""
This script takes an xls. file output of FreezeFrame results and organizes
them for analysis.
"""

import xlrd
wb = xlrd.open_workbook('C:\\Users\\ronni\\Desktop\\exp CFD.xls')
ws = wb.sheet_by_index(0)
# A list that will contain the ordered shock phase results
ordered_s = [[], [], [], [], [], [], [], []]
# A list that will contain the ordered non - shock phase results
ordered_ns = [[], [], [], [], [], [], [], []]
num_of_rows = ws.nrows - 1
# starting at 2 due to titles in 0 - 3
curr_row = 2
while curr_row < num_of_rows:
	curr_row += 1
	# The name of the trial, in the format of A day 1 R1 S 1-1,
	# A(condition A or B) day 1(num of day) R1(num of round, irrelevant here)
	#  S(phase, s or ns) 1-1 (cage num-animal num)
	cell_v = str(ws.cell_value(curr_row, 0))
	# Freezing time in seconds
	cell_r = str(ws.cell_value(curr_row, 1))
	day = int(cell_v[5]) - 1
	phase = cell_v[11]
	if phase == 's':
		animal = [cell_v[-3] + cell_v[-2] + cell_v[-1], cell_r]
		if len(ordered_s) == 0:
			ordered_s[day].append(animal)
		else:
			location = -1
			for i in xrange(len(ordered_s) - 1, -1, -1):
				if int(cell_v[-3]) < int(ordered_s[i][0][0]):
					location = i
				elif cell_v[-3] == ordered_s[i][0][0]:
					if cell_v[-1] < ordered_s[i][0][-1]:
						location = i
			if location == -1:
				ordered_s[day].append(animal)
			else:
				ordered_s[day].insert(location, animal)
	elif phase == 'n':
		animal = [cell_v[-3] + cell_v[-2] + cell_v[-1], cell_r]
		if len(ordered_ns) == 0:
			ordered_ns[day].append(animal)
		else:
			location = -1
			for i in xrange(len(ordered_ns) - 1, -1, -1):
				if int(cell_v[-3]) < int(ordered_ns[i][0][0]):
					location = i
				elif cell_v[-3] == ordered_ns[i][0][0]:
					if cell_v[-1] < ordered_ns[i][0][-1]:
						location = i
			if location == -1:
				ordered_ns[day].append(animal)
			else:
				ordered_ns[day].insert(location, animal)
	else:
		print 'This right here i a problem'
# From here exporting to a new organized .xls
import xlwt
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Results')
worksheet.write(3, 1, 'Day')
worksheet.write(3, 2, 'Animal')
worksheet.write(3, 3, '% Freezing')
worksheet.write(4, 0, 'Shock condition')
curr_row = 4
for i in ordered_s:
	for j in i:
		worksheet.write(curr_row, 2, j[0])
		worksheet.write(curr_row, 3, j[1])
		curr_row += 1
worksheet.write(curr_row, 0, 'Non - shock condition')
for i in ordered_ns:
	for j in i:
		worksheet.write(curr_row, 2, j[0])
		worksheet.write(curr_row, 3, j[1])
		curr_row += 1
# A table of the shock conditions over days
curr_row = 3
worksheet.write(1, 8, 'Shock condition')
worksheet.write(curr_row, 7, 'Animal')
worksheet.write(curr_row - 1, 8, 'Day')
for i in xrange(1, len(ordered_s) + 1):
	worksheet.write(3, i + 8, i)
for i in xrange(curr_row, 3 + len(ordered_s[0])):
	worksheet.write(i, 7, ordered_s[0][i - 3])
for i in xrange(0, len(ordered_s)):
	for j in xrange(0, len(ordered_s[0])):
		worksheet.write(j + 4, i + 2, ordered_s[i][j][1])
# A table of the non - shock conditions over day
curr_row = 30
worksheet.write(1, 8, 'Shock condition')
worksheet.write(curr_row, 7, 'Animal')
worksheet.write(curr_row - 1, 8, 'Day')
for i in xrange(1, len(ordered_s) + 1):
	worksheet.write(3, i + 8, i)
for i in xrange(curr_row, 3 + len(ordered_s[0])):
	worksheet.write(i, 7, ordered_s[0][i - 3])
for i in xrange(0, len(ordered_s)):
	for j in xrange(0, len(ordered_s[0])):
		worksheet.write(j + 4, i + 2, ordered_s[i][j][1])
workbook.save(r"C:\\Users\\ronni\\Desktop\\exp CFD organized.xls")