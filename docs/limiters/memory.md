# MemoryLimiter

- Description: In-Memory rate limiter that lives for the lifetime of the project runtime.

Pros:

- Fastest rate limiter since it lives in Python memory.
- No extra dependencies.

Cons:

- It makes the project stateful, meaning the rate limiter internal state is unique for each process running the project. If there are more than 1 process running the project, this rate limiter will fail.
- Rate limiter state is lost when the process is stopped or restarted.


## _class_ MemoryLimiter

Backend: `pyot.limiters.memory.MemoryLimiter`

Definitions:

* `__init__`
  * `limiting_share`: `int = 1`
