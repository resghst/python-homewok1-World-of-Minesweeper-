
# a = [[]*5 for i in range(0,9)]
a =[[[float(0) for k in range(3)] for j in range(9)] for i in range(9)]
# for i in range(0,9):
#     for j in range(0,9):
#         a[i][j] = [float(0),float(1),float(2)]
a[0][0][0] =3
for i in a:
    print i