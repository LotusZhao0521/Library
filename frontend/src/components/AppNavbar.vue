<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <div class="navbar-brand">
        <router-link to="/">📚 图书管理</router-link>
      </div>
      <div class="navbar-links">
        <router-link to="/" class="nav-link">图书列表</router-link>
        <router-link to="/my-borrows" class="nav-link">我的借阅</router-link>
        <template v-if="authStore.isAdmin">
          <router-link to="/admin/books" class="nav-link">图书管理</router-link>
          <router-link to="/admin/users" class="nav-link">用户管理</router-link>
        </template>
      </div>
      <div class="navbar-user">
        <router-link to="/change-password" class="nav-link user-name">
          {{ authStore.user?.username }}
        </router-link>
        <button class="btn-logout" @click="handleLogout">退出</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 0.5px solid rgba(0, 0, 0, 0.1);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 52px;
}

.navbar-brand a {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text);
  text-decoration: none;
}

.navbar-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  font-size: 14px;
  color: var(--color-text-secondary);
  text-decoration: none;
  padding: 6px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: var(--color-text);
  background: rgba(0, 0, 0, 0.04);
}

.nav-link.router-link-active {
  color: var(--color-primary);
  font-weight: 500;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.btn-logout {
  font-size: 13px;
  color: var(--color-text-tertiary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.08);
}
</style>
