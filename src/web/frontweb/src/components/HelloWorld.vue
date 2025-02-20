<template>
  <v-container fluid>
    <v-row>
      <!-- 左侧菜单 -->
      <v-col cols="3">
        <v-navigation-drawer permanent app width="250">
          <v-list nav dense>
            <v-list-item-group>
              <v-list-item v-for="(item, index) in menuItems" :key="index" :to="item.route">
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-navigation-drawer>
      </v-col>

      <!-- 右侧主要内容 -->
      <v-col cols="9">
        <v-card>
          <v-card-title>{{ msg }}</v-card-title>
          <v-card-text>
            For a guide and recipes on how to configure / customize this project,<br>
            check out the 
            <a href="https://cli.vuejs.org" target="_blank" rel="noopener">vue-cli documentation</a>.
          </v-card-text>

          <v-divider></v-divider>

          <!-- Installed CLI Plugins -->
          <v-card-subtitle>Installed CLI Plugins</v-card-subtitle>
          <v-list dense>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  <a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-babel" target="_blank" rel="noopener">babel</a>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  <a href="https://github.com/vuejs/vue-cli/tree/dev/packages/%40vue/cli-plugin-eslint" target="_blank" rel="noopener">eslint</a>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <!-- Essential Links -->
          <v-card-subtitle>Essential Links</v-card-subtitle>
          <v-list dense>
            <v-list-item v-for="(item, index) in essentialLinks" :key="index">
              <v-list-item-content>
                <v-list-item-title>
                  <a :href="item.href" target="_blank" rel="noopener">{{ item.title }}</a>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider></v-divider>

          <!-- Ecosystem -->
          <v-card-subtitle>Ecosystem</v-card-subtitle>
          <v-list dense>
            <v-list-item v-for="(item, index) in ecosystemLinks" :key="index">
              <v-list-item-content>
                <v-list-item-title>
                  <a :href="item.href" target="_blank" rel="noopener">{{ item.title }}</a>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      menuItems: [
        { title: '菜单项 1', icon: 'mdi-view-dashboard', route: '/' },
        { title: '菜单项 2', icon: 'mdi-account', route: '/profile' },
        { title: '菜单项 3', icon: 'mdi-settings', route: '/settings' }
      ],
      essentialLinks: [
        { title: 'Core Docs', href: 'https://vuejs.org' },
        { title: 'Forum', href: 'https://forum.vuejs.org' },
        { title: 'Community Chat', href: 'https://chat.vuejs.org' },
        { title: 'Twitter', href: 'https://twitter.com/vuejs' },
        { title: 'News', href: 'https://news.vuejs.org' }
      ],
      ecosystemLinks: [
        { title: 'vue-router', href: 'https://router.vuejs.org' },
        { title: 'vuex', href: 'https://vuex.vuejs.org' },
        { title: 'vue-devtools', href: 'https://github.com/vuejs/vue-devtools#vue-devtools' },
        { title: 'vue-loader', href: 'https://vue-loader.vuejs.org' },
        { title: 'awesome-vue', href: 'https://github.com/vuejs/awesome-vue' }
      ]
    }
  }
}
</script>

<style scoped>
/* 可根据需要添加自定义样式 */
</style>