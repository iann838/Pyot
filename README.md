# Pyot
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/pyot/blob/master/LICENSE)

Pyot is a Python Framework for the Riot Games API, including League of Legends, Teamfight Tactics, Legends of Runeterra and Valorant that encourages rapid development and clean, pragmatic design. It specializes at doing task in async environment to get the expected result faster than synchronous code. Thanks for checking it out.

Pyot is highly inspired by [Cassiopeia](https://github.com/meraki-analytics/cassiopeia), you will notice that both has similar internal workings. 

## Features

Features that Pyot has and can provide to your development.

- **_AsyncIO Based_**: No more waiting forever, concurrent calls and jobs made faster, highly configurable settings and wide range of tools to speed all your I/O tasks.
- **_Synchronous Compatible_**: An adapted version of Pyot that runs on synchronous environment, **Pyot will expose part of its API synchronously in its secondary module called Syot**.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, just add `pyot` to the installed apps and point your setting modules on your `settings.py` file.
- **_Community Projects Integrated_**: Take a step to dump the late and poor updated DDragon, we going beta testing directly using Cdragon and Meraki, BangingHeads' DDragon replacement is also coming soon.
- **_Caches Integrated_**: A wide range of Caches Stores is available right out of the box, we currently have Omnistone(Runtime), RedisCache(RAM), DiskCache(Disk) and MongoDB(NoSQL).
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics, Legends of Runeterra and Valorant.
- **_Autocompletion Included_**: Forget the standard dictionary keys, triple your code efficiency now with autocompletion enabled.
- **_Perfect Rate Limiter_**: Pyot Rate Limiter is production tested in all asynchronous, multithreaded and even multiprocessed environments, rate limiters for perfectionists.
- **_User Friendly Docs_**: Meet a friendly docs that "should" be easier to read and understand.

## About the Documentation

All documentation is in the "docs" directory and online at https://paaksing.github.io/Pyot/. If you're just getting started, here's how we recommend you read the docs:

> The documentation is separated into different pages at the top navbar.
> - **_Core_** section documents the core modules, objects and settings of Pyot.
> - **_Pipeline_** section documents the Low level API of Pyot's Pipeline objects.
> - **_Models_** section documents the objects APIs for each available model.
> - **_Stores_** section documents the available Stores configurable to the pipeline.
> - **_Limiters_** section documents the available Rate Limiters for the RiotAPI Store.
> - **_Utils_** section documents the available helper functions and objects of Pyot.
> - **_Developers_** section has contributing guidelines and wanted features.
>
> Portal: https://paaksing.github.io/Pyot/

1. First, read **Core > Introduction > Installation Guide** for instructions on installing Pyot.
2. Next, follow the quick start guide in **Core > Introduction > Quick Start Guide** for creating and running your first Pyot project.
3. Then you should get to know the types of objects that Pyot works with in **Core > Cores > Objects**.
4. Now give yourself an idea of what models we have and what objects we work in **Models**
5. You'll probably want to read through the topical context managers for achieving concurrency in **Core > Cores > Gatherer** and **Core > Cores > Queue**.
6. From there you can jump back to manipulating the settings by reading **Core > Cores > Settings** and get to know all the available pipeline stores in Pyot at **Stores**.
7. Check out all the utils objects and methods available in `pyot.utils` that can be handy in your development, documented at **Utils > Methods** and **Utils > Objects**.

Docs are updated rigorously. If you find any problems in the docs, or think they should be clarified in any way, please take 30 seconds to open an issue in this repository.

## To contribute to Pyot

Contributions are welcome! If you have idea or opinions on how things can be improved, don’t hesitate to let us know by posting an issue on GitHub or @ing me on the Riot API Discord channel. And we always want to hear from our users, even (especially) if it’s just letting us know how you are using Pyot.

Check out https://paaksing.github.io/Pyot/devs/ for information about getting involved.

Finally thanks for Django docs, I literally copied their doc format and changed the names. Yikes
