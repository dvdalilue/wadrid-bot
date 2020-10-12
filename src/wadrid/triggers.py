# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.engine.triggers import (
    BaseTrigger,
    Choice,
)

from .store import (
    cs,
    LoopContext,
    FrameContext,
)

class Loop(Choice):
    """
    Loop trigger

    Subclass of the 'Choice' trigger which extends the 'rank' method by altering
    the context to enter in a loop if the user's choice matches
    """

    def __init__(self, request, when):
        super().__init__(request, when)

    @cs.inject()
    async def rank(self, context) -> float:
        rank = await super().rank()
        loop_ctx = LoopContext(context)

        if rank and rank > .0:
            loop_ctx.enter_loop()

        return rank

class Bisector(Choice):
    """
    Bisector trigger

    Subclass of the 'Choice' trigger which extends the 'rank' method by checking
    the user's response, also if frame context has found an unique possible
    frame.
    """

    def __init__(self, request, upper_bound_choice):
        super().__init__(request, upper_bound_choice)
        self.choice = upper_bound_choice
        self.rocket_launched = None

    @cs.inject()
    async def rank(self, context) -> float:
        best = await super().rank()
        frame_ctx = FrameContext(context)

        if not self.slug and not best or frame_ctx.has_found():
            return .0

        self.rocket_launched = self.slug == self.choice

        return 1.

class FrameFound(BaseTrigger):
    """
    Frame found trigger

    Check whenever the frame context has found the final frame or not.
    """

    def __init__(self, request):
        super().__init__(request)

    @cs.inject()
    async def rank(self, context) -> float:
        frame_ctx = FrameContext(context)

        return 1. if frame_ctx.has_found() else .0
