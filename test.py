from datetime import datetime

# time1 = datetime(2021, 7, 20, 14, 20)
# time2 = datetime(2021, 7, 20, 20, 20)
# delta = time2 - time1
# print(delta, type(delta))
# print(str(delta).split(":")[0])

print(datetime.now())
print(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))