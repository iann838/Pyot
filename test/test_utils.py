import asyncio
import time

from pyot.models import lol
from pyot.utils.copy import fast_copy
from pyot.utils.functools import async_property, async_cached_property, async_generator_property
from pyot.utils.importlib import import_variable
from pyot.utils.itertools import frozen_generator
from pyot.utils.sync import async_to_sync, sync_to_async


def test_copy_fast_copy():
    o = {"1": 2, "3": 4}
    assert fast_copy(o) == o
    o = lol.Summoner(name="Morimorph")
    assert fast_copy(o).name == o.name


def test_importlib_import_variable():
    assert import_variable("pyot.models.lol.Match") is lol.Match
    assert import_variable("pyot.utils.importlib.import_variable") is import_variable


def test_itertools_frozen_generator():
    o_s = [lol.Summoner(name="Morimorph")] * 5
    for o in frozen_generator(o_s):
        assert o.name == "Morimorph"
        o.name = "SomethingElse"
    for o in frozen_generator(o_s):
        assert o.name == "Morimorph"


@async_to_sync
async def test_sync_sync_to_async():

    @sync_to_async
    def sleeper(secs):
        time.sleep(secs)

    start = time.time()
    await asyncio.gather(*[sleeper(i) for i in range(1, 5)])
    assert time.time() - start < 4.5


@async_to_sync
async def test_functools_async_properties():
    
    class A:
        b_count = 0
        @async_property
        async def a(self):
            return 0
        @async_cached_property
        async def b(self):
            self.b_count += 1
            return self.b_count
        @async_generator_property
        async def c(self):
            for i in range(10):
                yield i
        @async_generator_property
        async def d(self):
            for i in range(10):
                yield i, i * 2

    a = A()
    assert await a.a == 0
    assert await a.b == 1
    assert await a.b == 1
    assert await a.b == 1
    c_idx = 0
    async for c_i in a.c:
        assert c_i == c_idx
        c_idx += 1
    d_idx = 0
    async for d_i, d_i_2 in a.d:
        assert d_i == d_idx
        assert d_i_2 == d_idx * 2
        d_idx += 1
