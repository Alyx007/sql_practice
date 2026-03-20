"""All exercises in order."""

from .joins import exercise as joins
from .group_by import exercise as group_by
from .window_functions import exercise as window_functions
from .ctes import exercise as ctes
from .lag_lead import exercise as lag_lead
from .case_when import exercise as case_when
from .nulls import exercise as nulls

ALL = [joins, group_by, window_functions, ctes, lag_lead, case_when, nulls]
