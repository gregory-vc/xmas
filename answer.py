import pickle

with open('d.pkl', 'rb') as inp:
    d = pickle.load(inp)

import csv

# open the file in the write mode
f = open('submission.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file



writer.writerow(["oid","category"])

for k1 in d:
    m = []
    for k2 in d[k1]:
        m.append((d[k1][k2]["result"], k2))
    m = sorted(m, reverse=True)
    writer.writerow([k1, m[0][1]])


# close the file
f.close()