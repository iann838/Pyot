from pyot.utils import loop_run, timeit
from .manual_test_1 import pull_dev_key_limit, sync_dev_key_limit
from .manual_test_2 import pull_matchlist
from .speed_test_1 import iterate_match_events
import cProfile

# cProfile.run("loop_run(pull_matchlist())")
# loop_run(pull_matchlist())
loop_run(pull_dev_key_limit())

# print(timeit(iterate_match_events))
# cProfile.run("timeit(iterate_match_events, 100)")
