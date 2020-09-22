from pyot.utils import loop_run
from .manual_test_1 import pull_dev_key_limit
from .manual_test_2 import pull_matchlist
import cProfile

# cProfile.run("loop_run(pull_matchlist())")
# loop_run(pull_dev_key_limit())
loop_run(pull_matchlist())
