from .joins import challenges as joins
from .aggregation import challenges as aggregation
from .window import challenges as window
from .ctes import challenges as ctes

ALL = joins + aggregation + window + ctes
