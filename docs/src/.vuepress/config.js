const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'Pyot',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,
  
  base: "/Pyot/",

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#3eaf7c' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
  ],
  
  markdown: {
    lineNumbers: true
  },
  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  themeConfig: {
    repo: '',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: 'Last Updated',
    nav: [
      {
        text: 'Core',
        link: '/core/',
      },
      {
        text: 'Pipeline',
        link: '/pipeline/',
      },
      {
        text: 'Models',
        link: '/models/',
      },
      {
        text: 'Stores',
        link: '/stores/',
      },
      {
        text: 'Limiters',
        link: '/limiters/',
      },
      {
        text: 'Utils',
        link: '/utils/',
      },
      {
        text: 'Topics',
        link: '/topics/',
      },
      {
        text: 'Developers',
        link: '/devs/',
      },
      {
        text: 'Github',
        link: 'https://github.com/paaksing/pyot'
      },
      {
        text: 'VuePress',
        link: 'https://v1.vuepress.vuejs.org'
      }
    ],
    sidebar: {
      '/core/': [
        {
          title: 'Introduction',
          collapsable: false,
          children: [
            '',
            'installation',
            'startup',
          ]
        },
        {
          title: 'Integrations',
          collapsable: false,
          children: [
            'django',
            'celery',
            'syot',
          ]
        },
        {
          title: 'Cores',
          collapsable: false,
          sidebarDepth: 2,
          children: [
            'apiobjects',
            'settings',
            'gatherer',
            'queue',
            'exceptions',
          ]
        },
      ],
      '/pipeline/': [
        {
          title: 'Low Level API',
          collapsable: false,
          sidebarDepth: 2,
          children: [
            '',
            'token'
          ]
        },
        {
          title: 'Stores Bases',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'expiration',
            'handler',
            'object',
          ]
        }
      ],
      '/models/': [
        {
          title: 'General',
          collapsable: false,
          children: [
            ''
          ]
        },
        {
          title: 'Riot Services',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'riot_core',
            'riot_account',
            'riot_rso',
          ]
        },
        {
          title: 'League of Legends',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'lol_core',
            'lol_champion',
            'lol_championmastery',
            'lol_championrotation',
            'lol_clash',
            'lol_item',
            'lol_league',
            'lol_match',
            'lol_merakichampion',
            'lol_merakiitem',
            'lol_profileicon',
            'lol_rune',
            'lol_spectator',
            'lol_spell',
            'lol_summoner',
            'lol_status',
            'lol_thirdpartycode',
            'lol_tournaments',
          ]
        },
        {
          title: 'Teamfight Tactics',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'tft_core',
            'tft_champion',
            'tft_item',
            'tft_league',
            'tft_match',
            'tft_profileicon',
            'tft_summoner',
            'tft_thirdpartycode',
            'tft_trait',
          ]
        },
        {
          title: 'Legends of Runeterra',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'lor_core',
            'lor_card',
            'lor_match',
            'lor_ranked',
            'lor_status',
          ]
        },
        {
          title: 'Valorant',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'val_core',
            'val_content',
            'val_match',
            'val_status',
          ]
        }
      ],
      '/stores/': [
        {
          title: "General",
          collapsable: false,
          children: [
            '',
          ]
        },
        {
          title: "Stores",
          collapsable: false,
          children: [
            'omnistone',
            'djangocache',
            'rediscache',
            'diskcache',
            'mongodb',
            'cdragon',
            'ddragon',
            'merakicdn',
            'riotapi',
          ]
        }
      ],
      '/limiters/': [
        {
          title: "Low Level API",
          collapsable: false,
          sidebarDepth: 2,
          children: [
            '',
            'token'
          ]
        },
        {
          title: "Rate Limiters",
          collapsable: false,
          children: [
            'memory',
            'redis'
          ]
        }
      ],
      '/utils/': [
        {
          title: "Utils",
          collapsable: false,
          sidebarDepth: 1,
          initialOpenGroupIndex: 1,
          children: [
            '',
            'objects',
            'methods',
            'decorators',
          ]
        }
      ],
      '/topics/': [
        {
          title: "General",
          collapsable: false,
          children: [
            '',
          ]
        },
        {
          title: "Topics",
          collapsable: false,
          sidebarDepth: 2,
          initialOpenGroupIndex: 1,
          children: [
            'slow',
            'sudden_stop',
            'proactor_runtimeerror',
            'integrating',
            'why_not_asyncio_gather',
          ]
        }
      ],
      '/devs/': [
        '',
      ]
    }
  },

  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
  ]
}
