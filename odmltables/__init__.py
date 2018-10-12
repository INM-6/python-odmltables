import os
import json

here = os.path.dirname(__file__)

with open(os.path.join(here, "info.json")) as infofile:
    infodict = json.load(infofile)

VERSION = infodict["VERSION"]
