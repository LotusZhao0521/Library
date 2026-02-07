<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import AppNavbar from '@/components/AppNavbar.vue'

const authStore = useAuthStore()
</script>

<template>
  <div id="app">
    <AppNavbar v-if="authStore.isLoggedIn" />
    <main :class="{ 'with-nav': authStore.isLoggedIn }">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
main {
  min-height: 100vh;
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

main.with-nav {
  padding-top: 80px;
}
</style>
