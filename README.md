
> [!CAUTION]
> This package is now DEPRECATED and will no longer receive new updates. It has proved to be overly complex, hard to customize or extend, and contains an increased amount of implicit syntaxes that go against best practices. New projects shall NOT use this package and old projects should move away from this package as soon as possible.
> 
> The recommended package is [pulsefire](https://github.com/iann838/pulsefire). A modern and flexible Riot Games Python SDK. Built to be simple to use, highly configurable, and extendable. Objects and client responses are fully typed to speed up coding efficiency.

# Pyot

Pyot is an asyncIO-based high-level Python Riot Games API framework that encourages rapid development and clean, pragmatic design. It takes care of much of the hassle of the Riot Games API, so developers can focus on writing apps without reinventing the wheel. It’s free and open source.

| Index | Version |
| ---- | ------- |
| PyPI | `6.0.9` |
| master | `6.0.9` |

If you're migrating your project to a newer version of Pyot, please refer to the **Changelog** section of the [documentation](https://pyot.iann838.com).

## Features

Features that Pyot can provide for your projects.

- **_AsyncIO Based_**: Performing 60x faster with AsyncIO, highly configurable settings, and a wide range of tools to speed I/O tasks.
- **_Community Projects Integrations_**: Includes support for CDragon, MerakiCDN. DDragon for LoL is Forbidden due to incompatible APIs.
- **_Caches Integrated_**: A wide range of Caches Stores is available out of the box, and currently supports Omnistone(Runtime), RedisCache(RAM), DiskCache(Disk), and MongoDB(NoSQL).
- **_Multiple Models_**: Available models of League of Legends, Teamfight Tactics, Legends of Runeterra and VALORANT.
- **_Code Autocompletion_**: Access data through attributes and properties, and maximize code efficiency with code autocompletion.
- **_Perfect Rate Limiter_**: Pyot's Rate Limiter is production-tested in all asynchronous, multithreaded, and multiprocessed environments.
- **_User-Friendly Docs_**: Human readable documentation that covers guides and all the available high-level and low-level APIs in Pyot.

If this framework is useful, consider giving a **star** to the repo.

## Documentation

Portal: <https://pyot.iann838.com>

The documentation covers:

- Installation.
- Configuration.
- Base Objects.
- Concurrency Basics.
- Models API.
- Stores.
- Limiters.
- Utilities.
- Integrations.
- Issues.
- Changelog.

Due to the complexity of the framework, there is no quick-start guide, it is recommended to start with:

- Reading and understanding the **Cores** section of the documentation.
- Reading and understanding the example projects at **Examples** section to get familiar.
- If your project requires a specific integration, check out **Integrations** section.
