a = dict()

for i in range(1, 41, 2):
    for j in range(2, 41, 2):
        a[f"{i}"] = f"{j}"
        
print(a)
    