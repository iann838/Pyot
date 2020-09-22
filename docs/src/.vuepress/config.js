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
            'syot',
            'django',
          ]
        },
        {
          title: 'Core',
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
          title: 'Riot Service',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'riot_core',
            'riot_account',
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
            'lol_thirdpartycode',
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
          title: 'Valorant',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'val_core',
            'val_content',
            'val_match',
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
            'cdragon',
            'merakicdn',
            'riotapi'
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
