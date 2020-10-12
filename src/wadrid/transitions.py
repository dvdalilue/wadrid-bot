# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .triggers import *

transitions = [
    Tr(
        dest=S000xInitial,
        factory=CustomText.builder(its.WELCOME),
    ),
    Tr(
        origin=S000xInitial,
        dest=S000xInitial,
        factory=Loop.builder(when='no'),
    ),
    Tr(
        origin=S000xInitial,
        dest=S001xPrelude,
        factory=CustomChoice.builder('yes'),
    ),
    Tr(
        origin=S001xPrelude,
        dest=S000xInitial,
        factory=CustomChoice.builder('no'),
    ),
    Tr(
        dest=S002xFrame,
        factory=CustomText.builder(its.BEGIN),
    ),
    Tr(
        origin=S001xPrelude,
        dest=S002xFrame,
        factory=CustomChoice.builder('yes'),
    ),
    Tr(
        origin=S002xFrame,
        dest=S002xFrame,
        factory=Bisector.builder(upper_bound_choice='yes'),
    ),
    Tr(
        origin=S002xFrame,
        dest=S003xFinal,
        factory=FrameFound.builder(),
    ),
    Tr(
        origin=S003xFinal,
        dest=S000xInitial,
        factory=CustomChoice.builder('no'),
    ),
    Tr(
        origin=S003xFinal,
        dest=S002xFrame,
        factory=CustomChoice.builder('yes'),
    ),
    Tr(
        origin=S002xFrame,
        dest=S001xPrelude,
        factory=trg.Action.builder('cancel'),
    ),
]
