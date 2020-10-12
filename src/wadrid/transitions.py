# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.platforms.telegram import (
    platform as tgr,
)
from bernard.i18n import (
    intents as its,
)

from .states import *
from .triggers import *

transitions = [
    Tr(
        dest=S000xInitial,
        factory=trg.Text.builder(its.WELCOME),
    ),
    Tr(
        origin=S000xInitial,
        dest=S000xInitial,
        factory=Loop.builder(when='no'),
    ),
    Tr(
        origin=S000xInitial,
        dest=S001xPrelude,
        factory=trg.Choice.builder('yes'),
    ),
    Tr(
        origin=S001xPrelude,
        dest=S000xInitial,
        factory=trg.Choice.builder('no'),
    ),
    Tr(
        dest=S002xFrame,
        factory=trg.Text.builder(its.BEGIN),
    ),
    Tr(
        origin=S001xPrelude,
        dest=S002xFrame,
        factory=trg.Choice.builder('yes'),
    ),
    Tr(
        origin=S002xFrame,
        dest=S003xFrameInternal,
        factory=Bisector.builder(upper_bound_choice='yes'),
    ),
    Tr(
        origin=S002xFrame,
        dest=S004xFinal,
        factory=FrameFound.builder(),
    ),
    Tr(
        origin=S004xFinal,
        dest=S000xInitial,
        factory=trg.Choice.builder('no'),
    ),
    Tr(
        origin=S004xFinal,
        dest=S002xFrame,
        factory=trg.Choice.builder('yes'),
    ),
    Tr(
        origin=S003xFrameInternal,
        dest=S002xFrame,
        factory=trg.Anything.builder(),
        internal=True,
    ),
    Tr(
        origin=S002xFrame,
        dest=S001xPrelude,
        factory=trg.Action.builder('cancel'),
    ),
]
