from RsmaxUtils  import *
import asyncio
for i in range(1,10):
    asyncio.run(append_new_line("data.txt","hola run asicrono"+ str(i)))