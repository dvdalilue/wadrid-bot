# coding: utf-8
from bernard.engine.triggers import (
    BaseTrigger,
    Text,
    Choice,
)

from .store import (
    cs,
    FrameContext,
)

class TriggerContextMixin():
    """
    Trigger generic context

    This mixin encapsulates a dict-like behaviour
    """
    def get(self, key):
        self.trg_ctx = self.__dict__.get('trg_ctx', {})

        return self.trg_ctx.get(key)

    def set(self, key, value):
        self.trg_ctx = self.__dict__.get('trg_ctx', {})

        self.trg_ctx[key] = value

class CustomText(TriggerContextMixin, Text):
    """
    Custom text trigger

    Subclass of 'Text' trigger with trigger context mixin.
    """
    pass

class CustomChoice(TriggerContextMixin, Choice):
    """
    Custom choice trigger

    Subclass of 'Choice' trigger with trigger context mixin.
    """
    pass

class Loop(CustomChoice):
    """
    Loop trigger

    Subclass of 'CustomChoice' trigger which extends the 'rank' method by altering
    the context to enter in a loop if the user's choice matches
    """

    @cs.inject()
    async def rank(self, context) -> float:
        rank = await super().rank()

        if rank and rank > .0:
            self.set('loop', True)

        return rank

class Bisector(CustomChoice):
    """
    Bisector trigger

    Subclass of 'CustomChoice' trigger which extends the 'rank' method by
    checking if the frame context has found a result, otherwise asks for
    bisection.
    """

    def __init__(self, request, upper_bound_choice):
        super().__init__(request, upper_bound_choice)
        self.choice = upper_bound_choice

    @cs.inject()
    async def rank(self, context) -> float:
        best = await super().rank()

        if not self.slug and not best or FrameContext(context).has_found():
            return .0

        self.rocket_launched = self.slug == self.choice
        self.set('bisect', True)

        return 1.

class FrameFound(TriggerContextMixin, BaseTrigger):
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
