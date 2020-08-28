import pyot


def test_status():
    status = pyot.run(pyot.lol.Status(platform="na1").get())
    status.dict(pyotify=True)