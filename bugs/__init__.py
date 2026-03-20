from .join_bugs import bugs as join_bugs
from .aggregation_bugs import bugs as aggregation_bugs
from .logic_bugs import bugs as logic_bugs

ALL = join_bugs + aggregation_bugs + logic_bugs
