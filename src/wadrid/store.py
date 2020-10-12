# coding: utf-8
from bernard.conf import (
    settings,
)
from bernard.storage.context import (
    create_context_store,
)
from urllib.parse import (
    urljoin,
    quote,
)

import json
import aiohttp
import random

cs = create_context_store(ttl=0)

midpoint = lambda x, y: int((x + y) / 2)

class LoopContext():
    """
    Loop context manager

    Context abstraction to control and check a loop indicator.
    """

    def __init__(self, context):
        self.ctx = context

    def enter_loop(self):
        self.ctx['loop'] = True

    def exit_loop(self):
        self.ctx['loop'] = False

    def in_loop(self):
        return self.ctx['loop']

class FrameContext():
    """
    Frame context manager

    Context abstraction to handle frames related information and parameters.
    Defines initialization and configuration processes, properties accessors
    and implements a bisection algorithm.
    """

    def __init__(self, context):
        self.ctx = context

    async def init_context(self):
        self.clear()

        if not self.ctx.get('payload'):
            async with aiohttp.ClientSession() as session:
                url = urljoin(settings.FRAMEX_API_URL, 'video')

                if settings.FRAMEX_VIDEO_NAME:
                    url = urljoin(url, quote(settings.FRAMEX_VIDEO_NAME))

                async with session.get(url) as response:
                    data = await response.text()
                    payload = json.loads(data)

                    if not settings.FRAMEX_VIDEO_NAME:
                        payload = payload[0]

                    self.ctx['payload'] = payload


    def configure_context(self):
        payload = self.ctx['payload']

        self.ctx['video_name'] = quote(payload.get('name'))
        self.ctx['max_frame'] = payload.get('frames', 1) - 1
        self.ctx['min_frame'] = 0

        deviation = settings.FRAME_INITIAL_DEVIATION
        mid_frame = midpoint(self.ctx['max_frame'], self.ctx['min_frame'])
        frame_dev = int((self.ctx['max_frame'] - mid_frame) * deviation)

        self.ctx['frame'] = random.randint(
            mid_frame - frame_dev,
            mid_frame + frame_dev,
        )

    def get_current_frame(self):
        return self.ctx['frame']

    def set_current_frame(self, current_frame):
        self.ctx['frame'] = current_frame

    def get_image_url(self):
        video_name = self.ctx["video_name"]
        frame = self.ctx["frame"]

        url = urljoin(settings.FRAMEX_API_URL, f'video/{video_name}/')
        url = urljoin(url, f'frame/{frame}/')

        return url

    def get_max_frame(self):
        return self.ctx['max_frame']

    def get_min_frame(self):
        return self.ctx['min_frame']

    def set_max_frame(self, max_frame):
        self.ctx['max_frame'] = max_frame

    def set_min_frame(self, min_frame):
        self.ctx['min_frame'] = min_frame

    def bisect(self, to_upper_bound):
        if to_upper_bound:
            self.set_max_frame(self.get_current_frame())
        else:
            self.set_min_frame(self.get_current_frame())

        new_frame = midpoint(self.get_max_frame(), self.get_min_frame())
        self.set_current_frame(new_frame)

    def has_found(self):
        return self.ctx['min_frame'] + 1 >= self.ctx['max_frame']

    def clear(self):
        payload = self.ctx.get('payload')

        self.ctx.clear()

        self.ctx['payload'] = payload