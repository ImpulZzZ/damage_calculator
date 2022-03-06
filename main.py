import requests
import json
import sys
from modules.Ahri import Ahri


def main():
    ahri = Ahri()
    print(ahri.q(5,100))
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
