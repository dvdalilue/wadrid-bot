# coding: utf-8
from bernard import (
    layers as lyr,
)
from bernard.platforms.telegram import (
    layers as tgr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    intents as its,
)
from bernard.i18n import (
    translate as t,
)

from .store import (
    cs,
    LoopContext,
    FrameContext,
)

class WadridState(BaseState):
    """
    Root class for Wadrid.

    Here you must implement "error" and "confused" to suit your needs. They
    are the default functions called when something goes wrong. The ERROR and
    CONFUSED texts are defined in `i18n/en/responses.csv`.
    """

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(
            lyr.Markdown(t.HELP),
            lyr.Markdown(t.START_CMD),
            lyr.Markdown(t.SEARCH_CMD),
        )

    async def handle(self) -> None:
        raise NotImplementedError

    def reply_keyboard():
        """
        Common reply keyboard among the states. Two options "yes" or "no".
        """

        return tgr.ReplyKeyboard(
            keyboard=[
                [
                    tgr.KeyboardButton(
                        text='No',
                        choice='no',
                        intent=its.NO,
                    ),
                    tgr.KeyboardButton(
                        text='Yes',
                        choice='yes',
                        intent=its.YES,
                    )
                ],
            ],
            resize_keyboard=True,
        )

class S000xInitial(WadridState):
    """
    """

    @page_view('/bot/initial')
    @cs.inject()
    async def handle(self, context):
        name = await self.request.user.get_friendly_name()
        text = lyr.Text(t('WELCOME', name=name))
        loop_context = LoopContext(context)

        if loop_context.in_loop():
            text = lyr.Text(t.LOOP)
        else:
            await FrameContext(context).init_context()

        loop_context.exit_loop()
        context['started'] = False

        self.send(
            text,
            WadridState.reply_keyboard()
        )

class S001xPrelude(WadridState):
    """
    """

    @page_view('/bot/begin')
    @cs.inject()
    async def handle(self, context):
        text = lyr.Text(t.CONTINUE)

        if not context.get('started'):
            text = lyr.Text(t.BEGIN)
            FrameContext(context).configure_context()
            context['started'] = True

        self.send(text, WadridState.reply_keyboard())

class S002xFrame(WadridState):
    """
    """

    @page_view('/bot/search')
    @cs.inject()
    async def handle(self, context):
        url = FrameContext(context).get_image_url()

        cancel_kb = tgr.InlineKeyboard([
            [tgr.InlineKeyboardCallbackButton(
                text='Stop search',
                payload={ 'action': 'cancel' },
            )],
        ])

        self.send(lyr.Text(url), WadridState.reply_keyboard())
        self.send(lyr.Text(t.FRAME), cancel_kb)

class S003xFrameInternal(WadridState):
    """
    """

    @page_view('/bot/search/aux')
    @cs.inject()
    async def handle(self, context):
        frame_ctx = FrameContext(context)
        current_frame = frame_ctx.get_current_frame()

        if self.trigger.launched:
            frame_ctx.set_max_frame(current_frame)
        else:
            frame_ctx.set_min_frame(current_frame)

        frame_ctx.bisect()


class S004xFinal(WadridState):
    """
    """

    @page_view('/bot/final')
    @cs.inject()
    async def handle(self, context):
        frame_ctx = FrameContext(context)
        current_frame = frame_ctx.get_current_frame()

        frame_ctx.configure_context()

        self.send(
            lyr.Text(t('FINAL', frame=current_frame)),
            WadridState.reply_keyboard()
        )
