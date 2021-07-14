import pandas as pd



a = {
    "A": [1, 2, 3]
}

df = pd.DataFrame(a)
print(df.empty)
if not df.empty:
    print("yes")