"""Object-class registry."""

from .mean_sd import MeanSD
from .contingency import Contingency
from .histogram import Histogram
from .survival import Survival
from .table1 import Table1

REGISTRY = {
    MeanSD.object_class: MeanSD,
    Contingency.object_class: Contingency,
    Histogram.object_class: Histogram,
    Survival.object_class: Survival,
    Table1.object_class: Table1,
}


def make(object_class: str, inputs: dict, title: str = "",
         rounding: str = "2") -> "ScientificObject":
    from .base import ScientificObject
    cls = REGISTRY[object_class]
    return cls(inputs, title=title, rounding=rounding)
