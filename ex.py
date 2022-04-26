SET_CELLS = [[] for _ in range(3)]
print(SET_CELLS)
for i in range(0, len(SET_CELLS)):
    SET_CELLS[i].clear()
print(SET_CELLS)

SET_CELLS[2].append(12)

print(SET_CELLS)