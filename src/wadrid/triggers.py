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

    """

    def __init__(self, request, when):
        super().__init__(request, when)

    @cs.inject()
    async def rank(self, context) -> float:
        rank = await super().rank()
        loop_context = LoopContext(context)

        if rank and rank > .0:
            loop_context.enter_loop()

        return rank

class Bisector(Choice):
    """

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

    """

    def __init__(self, request):
        super().__init__(request)

    @cs.inject()
    async def rank(self, context) -> float:
        frame_ctx = FrameContext(context)

        return 1. if frame_ctx.has_found() else .0
