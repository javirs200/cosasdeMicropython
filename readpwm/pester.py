timeString = ""
currentTime = (1993, 8, 25, 1, 10, 10, 1, 1)
passtime = (1993, 8, 25, 1, 10, 11, 1, 10)
ms =  round(currentTime[5]*60000 + currentTime[6]*1000 + currentTime[7])
pms =  round(passtime[5]*60000 + passtime[6]*1000 + passtime[7])
passtime = currentTime
racetime = abs(pms - ms)
seconds = abs(round(racetime / 1000))
minutes = abs(round(racetime / 60000))
if (seconds > 59):
    seconds = seconds % 60
    minutes += round(seconds / 60)
    pass
milliseconds = racetime % 1000
if (minutes < 10):
    timeString += "0"
    pass
timeString += str(minutes)
timeString += ":"
if (seconds < 10):
    timeString += "0"
    pass
timeString += str(seconds)
timeString += "."
timeString += str(milliseconds)
print(str(timeString))