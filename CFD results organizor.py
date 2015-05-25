"""
This script takes an xls. file output of FreezeFrame results and organizes
them for analysis.
"""

KD = ['1-1', '1-3', '1-5', '2-2', '2-4', '3-1', '3-3', '3-5',
													'4-2',
				'4-4', '5-1', '5-3', '5-5', '6-2', '6-4']
import xlrd
wb = xlrd.open_workbook('C:\\Users\\ronni\\Desktop\\exp CFD g.xls')
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
	day = int(cell_v[6]) - 1
	phase = cell_v[11]
	if phase == 'S':
		current_phase = ordered_s
	elif phase == 'N':
		current_phase = ordered_ns
	animal = [cell_v[-3] + cell_v[-2] + cell_v[-1], cell_r]
	if len(current_phase[day]) == 0:
		current_phase[day].append(animal)
	else:
		location = -1
		for i in xrange(len(current_phase[day]) - 1, -1, -1):
			if int(cell_v[-3]) < int(current_phase[day][i][0][0]):
				location = i
			elif cell_v[-3] == current_phase[day][i][0][0]:
				if cell_v[-1] < current_phase[day][i][0][-1]:
					location = i
		if location == -1:
			current_phase[day].append(animal)
		else:
			current_phase[day].insert(location, animal)
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
# These re the pivot point for the table, they are the coordinates for the
# upper left corner. pr = pivot_rows, pc = pivot_columns
pr = 3
pc = 7
worksheet.write(pr + 1, pc + 1, 'Animal')
worksheet.write_merge(pr, pr, pc + 2, pc + 9, 'Day')
worksheet.write(pr - 1, pc, 'Shock condition')
for i in xrange(1, len(ordered_s) + 1):
	worksheet.write(pr + 1, pc + i + 1, i)
step_days = 2
step = 2
for i in ordered_s[0]:
	worksheet.write(pr + step, pc + 1, i[0])
	x = i[0]
	if i[0] in KD:
		worksheet.write(pr + step, pc, 'KD')
	else:
		worksheet.write(pr + step, pc, 'Scr')
	step += 1
worksheet.write(pr + step, pc, 'STDDEV:')
worksheet.write(pr + step + 1, pc, 'SEM:')
worksheet.write(pr + step + 2, pc, 'Mean:')
for i in ordered_s:
	step = 2
	for j in i:
		worksheet.write(pr + step, pc + step_days, j[1])
		step += 1
	step_days += 1
pr += 35
worksheet.write(pr + 1, pc + 1, 'Animal')
worksheet.write_merge(pr, pr, pc + 2, pc + 9, 'Day')
worksheet.write(pr - 1, pc, 'Non - shock condition')
for i in xrange(1, len(ordered_ns) + 1):
	worksheet.write(pr + 1, pc + i + 1, i)
step_days = 2
step = 2
for i in ordered_s[0]:
	worksheet.write(pr + step, pc + 1, i[0])
	if i[0] in KD:
		worksheet.write(pr + step, pc, 'KD')
	else:
		worksheet.write(pr + step, pc, 'Scr')
	step += 1
worksheet.write(pr + step, pc, 'STDDEV:')
worksheet.write(pr + step + 1, pc, 'SEM:')
worksheet.write(pr + step + 2, pc, 'Mean:')
for i in ordered_ns:
	step = 2
	for j in i:
		worksheet.write(pr + step, pc + step_days, j[1])
		step += 1
	step_days += 1
workbook.save(r"C:\\Users\\ronni\\Desktop\\exp CFD organized.xls")
