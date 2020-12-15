# Why not use asyncio.gather

Well, if you already tried, you must suffered these problems:

* Tasks takes centuries to start
* The tasks breaks randomly
* CPU is going insane

That is because `asyncio.gather` will try to schedule all the tasks that you dump in it, before even executing one of them, if you dump 20k tasks in it, you are running 20k tasks at once. So these managers are in pyot just to counter these situations:

* Gatherer: This manager will split your tasks into chunks and consume them chunk by chunk
* Queue: This manager will consume your tasks one by one as you `put` into it.
