<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5">
          <v-card-title>
            About Page
          </v-card-title>
          <v-card-text>
            <h1>This is an about page</h1>
            <p>下面是几个 Vuetify 组件示例：</p>
            <v-btn color="primary" @click="handleClick">点击我</v-btn>
            <v-btn color="success" @click="handleClick">再试试看啊</v-btn>
            <v-alert type="success" border="left" colored-border>
              成功警告组件示例
            </v-alert>
            <v-progress-linear indeterminate color="secondary"></v-progress-linear>
          </v-card-text>
          <v-card-actions>
            <v-btn text>了解更多</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AboutView',
  methods: {
    handleClick() {
      console.log('按钮被点击了')
    },
  },
}
</script>

<style scoped>
.about {
  margin: 20px;
}
</style>