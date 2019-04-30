

data = open("expvolume.20190426.txt").read().split()


carCo = [i for i, e in enumerate(data) if e == 'TSLA']
print(carCo)
for x in carCo[0::2]:
    print("Underlying Symbol ", data[x+1][0:5])
