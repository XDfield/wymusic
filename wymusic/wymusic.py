import os
from wymusic import api, CONST


def main():
    if not os.path.exists(CONST.BASEPATH):
        os.mkdir(CONST.BASEPATH)
    api.playDaily()

if __name__ == '__main__':
    main()
