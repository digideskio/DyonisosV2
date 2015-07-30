__author__ = 'Maxime'

import sys
from appclass import appclass
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    app = appclass()
    app.run()

if __name__ == '__main__':
    main()