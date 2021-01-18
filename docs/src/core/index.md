# Pyot
##### <Badge text="Stable" vertical="middle"/> [<Badge text="MIT Licensed" type="warning" vertical="middle"/>](https://github.com/paaksing/pyot/blob/master/LICENSE)

Pyot is an asyncIO based high-level Python Riot Games API framework that encourages rapid development and clean, pragmatic design. Built by experienced Riot Games Third Party Developers, it takes care of much of the hassle of the Riot Games API, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

### Pyot 3

- Code will run 3 ~ 5 times faster compared to Pyot 2.
- Support for RoleML and Roleidentification.
- Refactored objects to use non-destructive design.

Migration Guide: [Version 2 → 3](v2tov3.html)

## Features

Features that Pyot has and can provide to your development.

- **_AsyncIO Based_**: Go 60x faster with asyncIO and coroutines, highly configurable settings and wide range of tools to speed your I/O tasks.
- **_Django Support_**: Full support for Django Caches Framework and its new 3.1 async Views, enable as installed app and point your setting modules on your `settings.py` file. [More details](django.html).
- **_Community Projects Integrated_**: Includes support for CDragon, MerakiCDN, RoleML, RoleIdentification. DDragon is Forbidden due to incompatible APIs.
- **_Caches Integrated_**: A wide range of Caches Stores is available right out of the box, we currently have Omnistone(Runtime), RedisCache(RAM), DiskCache(Disk) and MongoDB(NoSQL).
- **_Multiple Models_**: Available models are League of Legends, Teamfight Tactics, Legends of Runeterra and VALORANT.
- **_Code Autocompletion_**: Access data through attributes and properties, maximize your code efficiency now with autocompletion.
- **_Perfect Rate Limiter_**: Pyot's Rate Limiter is production tested in all asynchronous, multithreaded and even multiprocessed environments. Pyot's rate limiters are made for perfectionists.
- **_User Friendly Docs_**: Meet a human redable documentation that covers guides and all the available high-level and low-level APIs in Pyot.
- **_Synchronous Compatible_**: An adapted version of Pyot that runs on synchronous environment, exposing part of its API synchronously on [Syot](syot.html).

## About the Documentation

All documentation is in the "docs" directory. If you're just getting started, here's how we recommend you read the docs:

> The documentation is separated into different pages at the top navbar.
> - **_Core_** section documents the core modules, objects and settings of Pyot.
> - **_Pipeline_** section documents the Low level API of Pyot's Pipeline objects.
> - **_Models_** section documents the objects APIs for each available model.
> - **_Stores_** section documents the available Stores configurable to the pipeline.
> - **_Limiters_** section documents the available Rate Limiters for the RiotAPI Store.
> - **_Utils_** section documents the available helper functions and objects of Pyot.
> - **_Topics_** section documents common Q&As and hard touched topics of Pyot.
> - **_Developers_** section has contributing guidelines and wanted features.

1. First, read the **[Installation Guide](installation.html)** for instructions on installing Pyot.
2. Next, follow the quick start guide in **[Quick Start Guide](startup.html)** for creating and running your first Pyot project.
3. Then you should get to know the types of objects that Pyot works with in **[Objects](apiobjects.html)**.
4. Now give yourself an idea of what models we have and what objects we work in **[Models](/models/)**
5. You'll probably want to read through the topical context managers for achieving concurrency in **[Gatherer](gatherer.html)** and **[Queue](queue.html)**.
6. From there you can jump back to manipulating the settings by reading **[Settings](settings.html)** and get to know all the available pipeline stores in Pyot at **[Stores](/stores/)**.
7. Check out all the utils objects and methods available in `pyot.utils` that can be handy in your development, documented at **[Utils](/utils/)**.

Docs are updated rigorously. If you find any problems in the docs, or think they should be clarified in any way, please take 30 seconds to open an issue in this repository.

## To contribute to Pyot

If this framework is useful to you, a **star** to the repo is appreciated.

Contributions are welcome! If you have ideas or opinions on how things can be improved, don’t hesitate to let us know by posting an issue on GitHub or @ing me on the Riot API Discord channel. We always want to hear from our users, even (especially) if it’s just letting us know how you are using Pyot.

Check out [Developers](/devs/) for contributing.

Finally thanks for Django docs, I literally copied their doc format and changed the names. Yikes
