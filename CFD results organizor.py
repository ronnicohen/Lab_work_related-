import xlrd
wb = xlrd.open_workbook('C:\\Users\\ronni\\Desktop\\exp CFD.xls')
ws = wb.sheet_by_index(0)
ordered = []
num_of_rows = ws.nrows - 1
curr_row = 2
while curr_row < num_of_rows:
	curr_row += 1
	cell_v = str(ws.cell_value(curr_row, 0))
	cell_r = str(ws.cell_value(curr_row, 1))
	animal = [cell_v[-3] + cell_v[-2] + cell_v[-1], cell_r]
	if len(ordered) == 0:
		ordered.append(animal)
	else:
		location = -1
		for i in xrange(len(ordered) - 1, -1, -1):
			if int(cell_v[-3]) < int(ordered[i][0][0]):
				location = i
			elif cell_v[-3] == ordered[i][0][0]:
				if cell_v[-1] < ordered[i][0][-1]:
					location = i
		if location == -1:
			ordered.append(animal)
		else:
			ordered.insert(location, animal)
