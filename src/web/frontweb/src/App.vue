<template>
  <v-app>
    <!-- 顶部导航栏 -->
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>My App</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/" tag="router-link">Home</v-btn>
      <v-btn text to="/about" tag="router-link">About</v-btn>
    </v-app-bar>

    <!-- 主要内容区域 -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- 页脚 -->
    <v-footer app color="primary" dark>
      <v-col class="text-center white--text">
        &copy;2025 My App
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style>
html,
body,
#app,
.v-application {
  height: 100%;
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}
</style>