# My tasks suddently stopped

For you to know that your tasks stopped in the middle of it, you most likely have the `LOG_LEVEL` higher than 20, or the actual tasks is not giving the expected output.

## Situations that it might have stopped

Rated from high to low probability

1. ***Issue:*** Most of the time the tasks didn't stop, it was just chilling waiting for your rate limits to update a bucket. ***Solution:*** Wait it out or ask a higher limit in the Riot Dev Portal.
2. ***Issue:*** You caused memory leakage hitting the OS per process RAM limit and python aborted some of the objects. ***Solution:*** Avoid loading all the objects into the memory (python runtime), create a function or method that can consume the object while loading it and garbage it afterwards, there is a detailed warning and examples in both **[Gatherer](/core/gatherer.html)** and **[Queue](/core/queue.html)**.
3. ***Issue:*** There is a synchorous task running that blocks the event loop giving no chance at all to the task. ***Solution:*** Nuke the task, and make it run in another process or thread.
4. ***Issue:*** It is very unlikely that Pyot itself will cause your tasks to stop, but it's not warrantied to be a non-zero chance from happening. ***Solution:*** Try cleaning the redis db if you're using `RedisLimiter` for your rate limits and make a clean up of the storages that pyot interacts with.
5. ***Issue:*** You're running the thing in a potato that suddenly went out of power or crashed. ***Solution:*** Run it in an actual computer.
