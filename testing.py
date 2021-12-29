import time
t = time.localtime()
current_time = str(time.strftime("%m/%d/%Y, %H:%M:%S",t))

print(current_time)
print(type(current_time))

