from pyot.utils import loop_run
from pyot.models import lol


def test_status():
    status = loop_run(lol.Status(platform="na1").get())
    status.dict(pyotify=True)