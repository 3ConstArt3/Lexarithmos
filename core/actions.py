# -*- coding: utf-8 -*-
from enum import Enum


class Action(Enum):

    """
    Represents the available user actions
    inside the Lexarithmos application.
    """

    COMPUTE_ONLY = "compute_only"
    INSERT = "insert"
    DELETE = "delete"
