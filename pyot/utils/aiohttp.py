import asyncio
import functools
import warnings

from aiohttp import ClientSession


warnings.filterwarnings('ignore', category=DeprecationWarning)


class SafeClientSession(ClientSession):

    def _create_closed_event(self) -> asyncio.Event:
        """
        Work around aiohttp issue that doesn't properly close transports on exit.
        See https://github.com/aio-libs/aiohttp/issues/1925#issuecomment-639080209
        """

        transports = 0
        all_is_lost = asyncio.Event()

        def connection_lost(exc, orig_lost):
            nonlocal transports
            try:
                orig_lost(exc)
            finally:
                transports -= 1
                if transports == 0:
                    all_is_lost.set()

        def eof_received(orig_eof_received):
            try:
                orig_eof_received()
            except AttributeError:
                # eof_received() is called after _app_protocol and _transport are set to None
                pass

        for conn in self.connector._conns.values():
            for handler, _ in conn:
                proto: asyncio.Protocol = getattr(handler.transport, "_ssl_protocol", None)
                if proto is None:
                    continue
                transports += 1
                orig_lost = proto.connection_lost
                orig_eof_received = proto.eof_received
                proto.connection_lost = functools.partial(
                    connection_lost, orig_lost=orig_lost
                )
                proto.eof_received = functools.partial(
                    eof_received, orig_eof_received=orig_eof_received
                )

        if transports == 0:
            all_is_lost.set()

        return all_is_lost

    async def close(self) -> None:
        '''Graceful close and release all resources.'''
        closed_event = self._create_closed_event()
        await super().close()
        await closed_event.wait()


warnings.filterwarnings('default', category=DeprecationWarning)
