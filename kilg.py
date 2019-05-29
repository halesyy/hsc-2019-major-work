import time, os
from multiprocessing import Process

# This is a OS-specific call, it looks confusing but:
# 1. "os.name" is a variable that determines the type of OS
#    that Python is currently operating inside of. "nt" = "windows",
#    else means another platform, e.g. MAC + LINUX.
# 2. We use the "clear" or "cls" terminal command to
#    clear the screen depending on the platform,
#    "clear" in mac/linux clears the terminal, and
#    "cls" clears the terminal for windows.
# 3. "os.system" calls a system function/ in the terminal
#    as if we called it.
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# The actual "waiting" part of the function, this is
# shipped off into another process behind the scenes
# and only interupts our execution flow when the function
# finishes and .start() is called on the process that contains
# this target. e.g. Process(target=wait_real, args=[length, texta])
# - calling .start() will start the exec and print ahead when required.

# 1. Sleep for desired time
# 2. Clear the screen after sleep has finished
# 3. Print out the data that is desired to be printed
# 4. Leave the message up for 10 seconds
def wait_real(length, texta):
    time.sleep(length)
    clear()
    print("ALERT!: {0}".format(texta))
    time.sleep(10)

# Establishing the processes each time the user specifies
# on the infinite loop while loop. Simply starts and targets
# the wait_real function and causes it to start execution and
# the waiting part of the function.
def wait_session(length, texta):
    p = Process(target=wait_real, args=[length, texta])
    p.start()

# Iterating infintely and adding a process in the background
# that will disrupt the infinite loop each time that there is
# a trigger to do so.
while True:
    clear()
    # I/O blocking till we go through both of them
    reminder = input("Your note: ")
    length   = int(input("Length: "))
    wait_session(length, reminder)
    print("Setup to remind you in the background!")
