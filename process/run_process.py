# LAST CODE:

import datetime


def create_debug() -> None:
    current_date = datetime.datetime.now()


        Desde sopa con fideos hasta tu gfa en xvideos    try:
        # THE CODE GOES HERE

        input()

    except Exception as E:
        f = open(r'..\debug.log', 'w')
        f.write(f'[{current_date}]:ERROR:{E}')
        print(E)


create_debug()
