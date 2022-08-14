import asyncio
import sys

from module.tasks import average_win_rate_10_matches


if __name__ == "__main__":
    print("Summoner name:", sys.argv[1])
    average_win_rate = asyncio.run(average_win_rate_10_matches(sys.argv[1]))
    print(
        "Average win rate (last 10 matches):",
        average_win_rate * 100, "%"
    )
