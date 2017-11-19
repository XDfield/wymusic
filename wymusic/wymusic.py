import os
import sys
import getopt

import wyapi
import CONST


def main():
    if not os.path.exists(CONST.BASEPATH):
        os.mkdir(CONST.BASEPATH)
    mode = 'single'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l')
    except getopt.GetoptError:
        sys.exit()
    for opt, arg in opts:
        if opt in ('-l',):
            mode = 'loop'
    wyapi.playDaily(mode)


if __name__ == '__main__':
    main()
