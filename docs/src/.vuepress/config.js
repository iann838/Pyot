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
    lastUpdated: false,
    nav: [
      {
        text: 'Framework Cores',
        link: '/cores/',
      },
      {
        text: 'Models API',
        link: '/api/',
      },
      {
        text: 'Pipeline Stores',
        link: '/stores/',
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
      '/cores/': [
        {
          title: 'Introduction',
          collapsable: false,
          children: [
            ''
          ]
        },
        {
          title: 'Pyot',
          collapsable: false,
          sidebarDepth: 2,
          children: [
            'apiobjects',
            'settings',
            'pipeline',
            'gatherer',
          ]
        },
        {
          title: 'Syot',
          collapsable: false,
          children: [
            'syot'
          ]
        },
        {
          title: 'Djot',
          collapsable: false,
          children: [
            'djot'
          ]
        },
      ],
      '/api/': [
        {
          title: 'Introduction',
          collapsable: false,
          children: [
            ''
          ]
        },
        {
          title: 'League of Legends',
          collapsable: false,
          sidebarDepth: 1,
          children: [
            'lol_account',
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
            'tft_account',
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
            'val_account',
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
            'expiration',
            'handler',
          ]
        },
        {
          title: "Stores",
          collapsable: false,
          children: [
            'omnistone',
            'djangocache',
            'cdragon',
            'merakicdn',
            'riotapi'
          ]
        }
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
