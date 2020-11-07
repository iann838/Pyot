from pyot.models import lor
from pyot.utils import loop_run

async def async_card(card=None):
    if card is None:
        card = await lor.Card(code="03BW014", locale="en_us").get()
    assert isinstance(card.region, str)
    assert isinstance(card.region_ref, str)
    assert isinstance(card.attack, int)
    assert isinstance(card.cost, int)
    assert isinstance(card.health, int)
    assert isinstance(card.description, str)
    assert isinstance(card.description_raw, str)
    assert isinstance(card.levelup_description, str)
    assert isinstance(card.levelup_description_raw, str)
    assert isinstance(card.flavor_text, str)
    assert isinstance(card.artist_name, str)
    assert isinstance(card.name, str)
    assert isinstance(card.code, str)
    assert isinstance(card.spell_speed, str)
    assert isinstance(card.spell_speed_ref, str)
    assert isinstance(card.rarity, str)
    assert isinstance(card.rarity_ref, str)
    assert isinstance(card.subtype, str)
    assert isinstance(card.supertype, str)
    assert isinstance(card.type, str)
    assert isinstance(card.collectible, bool)
    assert isinstance(card.set, int)
    assert isinstance(card.faction, str)
    assert isinstance(card.number, int)
    for keyword in card.keywords:
        assert isinstance(keyword, str)
    for keyword in card.keyword_refs:
        assert isinstance(keyword, str)
    for subtype in card.subtypes:
        assert isinstance(subtype, str)
    for code in card.associated_card_codes:
        assert isinstance(code, str)
    for asset in card.assets:
        assert isinstance(asset.full_absolute_path, str)
        assert isinstance(asset.game_absolute_path, str)

async def async_cards():
    cards = await lor.Cards(set=3).get()
    for card in cards:
        await async_card(card)

def test_card():
    loop_run(async_card())

def test_cards():
    loop_run(async_cards())

def test_deck():
    d = lor.Deck(code='CEBAIAIFB4WDANQIAEAQGDAUDAQSIJZUAIAQCBIFAEAQCBAA')
    raw = d.decode().raw
    for code in ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052', '2:01SI005', '2:01FR004']:
        assert code in raw
    encoded = d.encode()
    raw = d.decode().raw
    for code in ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052', '2:01SI005', '2:01FR004']:
        assert code in raw
    d = lor.Deck(code='CIBAIAIFB4WDANQIAEAQGDAUDAQSIJZUAIAQCAIEAEAQKBIA')
    raw = d.decode().raw
    for code in ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052', '2:01SI005', '2:01FR004']:
        assert code in raw
    for batch in d:
        assert isinstance(batch, lor.Batch)
        assert batch.count > 0 and batch.count <= 3
        assert isinstance(batch.code, str)
    deck = lor.Deck()
    for code in ['3:01SI015', '3:01SI044', '3:01SI048', '3:01SI054', '3:01FR003', '3:01FR012', '3:01FR020', '3:01FR024', '3:01FR033', '3:01FR036', '3:01FR039', '3:01FR052', '2:01SI005', '2:01FR004']:
        deck.append(lor.Batch(raw=code))
    deck.pop()
    deck.append(lor.Batch(code="01FR004", count=2))
    assert deck.encode() == encoded
    deck.pull('01FR004')
    deck.append(lor.Batch(code="01FR004", count=2))
    assert deck.encode() == encoded
