"""Quickstart: encode a 2x2 object at L3 and validate it."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from summarycodec.objects import make
from summarycodec.core.codec import encode
from summarycodec.core import Level
from summarycodec.validators import validate
from summarycodec.decoders import decode

inputs = {"cells": [[42, 158], [19, 181]],
          "row_labels": ["treated", "control"],
          "col_labels": ["event", "no event"]}

obj = make("contingency", inputs, title="Treatment x outcome")
encode(obj, "svg", Level.L3, "example_2x2.svg", actor="quickstart")
print(validate("example_2x2.svg").status.value)          # VALID
print(json.dumps(decode("example_2x2.svg")["displayed"], indent=1))

# secondary analysis straight from the published object
o2 = make("contingency", decode("example_2x2.svg")["inputs"])
print(o2.secondary_queries()["odds_ratio_recomputed"]())
