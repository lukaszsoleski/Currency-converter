from os.path import join,normpath, abspath,dirname
from enum import Enum


ROOT_DIR = dirname(abspath(__file__))

IMAGES_DIR = normpath(join(ROOT_DIR,r"data/resources/images"))

RESOURCES_DIR = normpath(join(ROOT_DIR,r"data/resources"))

CURRENCIES_FILE_PATH = normpath(join(RESOURCES_DIR,"currencies.txt"))

APP_ICON = normpath((join(IMAGES_DIR,"appicon.gif")))
class Currency(Enum):
    PLN = "PLN"
    EUR = "EUR"
    USD = "USD"
    AUD = "AUD"
    GBP = "GBP"
    CAD = "CAD"
    HKD = "HKD"
    JPY = "JPY"
    CHF = "CHF"


class Flag(Enum):
    PLN = normpath(join(IMAGES_DIR,"PLN.png"))
    EUR = normpath(join(IMAGES_DIR,"EUR.png"))
    USD = normpath(join(IMAGES_DIR,"USD.png"))
    AUD = normpath(join(IMAGES_DIR,"AUD.png"))
    GBP = normpath(join(IMAGES_DIR,"GBP.png"))
    CAD = normpath(join(IMAGES_DIR,"CAD.png"))
    HKD = normpath(join(IMAGES_DIR,"HKD.png"))
    JPY = normpath(join(IMAGES_DIR,"JPY.png"))
    CHF = normpath(join(IMAGES_DIR,"CHF.png"))

