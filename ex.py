rows=2
cols=4
B = [[[] for i in range(0,cols)] for j in range(0,rows)]

#print(B)
for i in B:
    print(i)

for i in range(0, rows):
    for j in range(0, cols):
        B[i][j].append(f"{i}{j}")

for i in range(0,rows):
    print(B[i])


