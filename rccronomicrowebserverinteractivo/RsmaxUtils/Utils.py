print("utils imported")

async def append_new_line(file_name, text_to_append):
    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


async def sendData(ws):
    try:
        fname = "data.txt"
        with open(fname, "r") as file_object:
            Lines = file_object.readlines()
            for l in Lines:
                ws.SendTextMessage(str(l))
    except:  # open failed
        pass


def isclose(a, b, rel_tol=1e-09, abs_tol=50.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


pass


def formatTime(racetime: int) -> str:
    ts = ""
    seconds = abs(round(racetime / 1000000))
    minutes = abs(round(racetime / 60000000))
    if (seconds > 59):
        seconds = seconds % 60
        minutes += round(seconds / 60)
        pass
    milliseconds = racetime % 1000
    if (minutes < 10):
        ts += "0"
        pass
    ts += str(minutes)
    ts += ":"
    if (seconds < 10):
        ts += "0"
        pass
    ts += str(seconds)
    ts += "."
    ts += str(milliseconds)

    return ts


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever
