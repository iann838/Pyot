from concurrent.futures import ThreadPoolExecutor
import warnings

from pyot.core.resources import resource_manager, resource_managed_loops
from pyot.core.queue import Queue
from pyot.core.warnings import PyotResourceWarning
from pyot.models import lol
from pyot.utils.sync import async_to_sync

from .engine_core import assert_types, assert_walkable


@async_to_sync
async def test_resource_and_queue():
    async with resource_manager():
        assert len(resource_managed_loops) == 1
        async with Queue() as queue:
            o = await lol.Summoner(name="Morimorph").get()
            h = await o.match_history.get()
            for m in h.matches[:5]:
                await queue.put(m.get())
            ms = await queue.join()
        assert len(ms) == 5
        assert_walkable(o)
        assert_types(o)
    assert len(resource_managed_loops) == 0


@async_to_sync
async def test_resource():
    async with resource_manager():
        o = await lol.Summoner(name="Morimorph").get()
    assert len(resource_managed_loops) == 0
    assert_walkable(o)
    assert_types(o)


def test_resource_multithread():

    @async_to_sync
    async def inner():
        async with resource_manager(), Queue() as queue:
            o = await lol.Summoner(name="Morimorph").get()
            h = await o.match_history.get()
            for m in h.matches[:5]:
                await queue.put(m.get())
            ms = await queue.join()
        assert len(ms) == 5
        for o in ms:
            assert_walkable(o)
            assert_types(o)

    @async_to_sync
    @resource_manager.as_decorator
    async def inner_decorated():
        async with Queue() as queue:
            o = await lol.Summoner(name="Morimorph").get()
            h = await o.match_history.get()
            for m in h.matches[:5]:
                await queue.put(m.get())
            ms = await queue.join()
        assert len(ms) == 5
        for o in ms:
            assert_walkable(o)
            assert_types(o)

    warnings.filterwarnings("error")
    futures = []
    with ThreadPoolExecutor() as executor:
        for _ in range(3):
            futures.append(executor.submit(inner))
            futures.append(executor.submit(inner_decorated))
        for future in futures:
            future.result()
    warnings.filterwarnings("default")


def test_resource_multithread_fail_missing():

    @async_to_sync
    async def inner():
        async with Queue() as queue:
            o = await lol.Summoner(name="Morimorph").get()
            h = await o.match_history.get()
            for m in h.matches[:5]:
                await queue.put(m.get())
            ms = await queue.join()
        assert len(ms) == 5
        for o in ms:
            assert_walkable(o)
            assert_types(o)

    warnings.filterwarnings("error")
    futures = []
    with ThreadPoolExecutor() as executor:
        for _ in range(5):
            futures.append(executor.submit(inner))
        for future in futures:
            try:
                future.result()
            except PyotResourceWarning:
                assert True
    warnings.filterwarnings("default")


def test_resource_multithread_fail_exists():

    async def inner_squared(m: lol.Match):
        async with resource_manager():
            return await m.get()

    @async_to_sync
    async def inner():
        async with resource_manager(), Queue() as queue:
            o = await lol.Summoner(name="Morimorph").get()
            h = await o.match_history.get()
            o = await inner_squared(h.matches[0])
        assert_walkable(o)
        assert_types(o)

    warnings.filterwarnings("error")
    futures = []
    with ThreadPoolExecutor() as executor:
        for _ in range(5):
            futures.append(executor.submit(inner))
        for future in futures:
            try:
                future.result()
                assert False
            except RuntimeError as e:
                assert "already" in str(e)
    warnings.filterwarnings("default")
