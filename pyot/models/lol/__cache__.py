from collections import defaultdict
from pyot.utils import AutoData

# pylint: disable=unused-import

try:
    import roleml
except (ImportError, ValueError) as e:
    roleml = e

try:
    import roleidentification
    champion_roles = AutoData(lambda: defaultdict(lambda: {}, roleidentification.pull_data()))
except ImportError as e:
    roleidentification = champion_roles = e
