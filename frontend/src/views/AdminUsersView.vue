<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { User } from '@/types'
import { userApi } from '@/api'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const users = ref<User[]>([])
const loading = ref(true)
const showModal = ref(false)
const saving = ref(false)

const form = ref({
  username: '',
  password: '',
  role: 'user',
})

async function fetchUsers() {
  loading.value = true
  try {
    const { data } = await userApi.list()
    users.value = data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.value = { username: '', password: '', role: 'user' }
  showModal.value = true
}

async function handleCreate() {
  saving.value = true
  try {
    await userApi.create(form.value)
    showModal.value = false
    await fetchUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || '创建失败')
  } finally {
    saving.value = false
  }
}

async function toggleRole(user: User) {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  const action = newRole === 'admin' ? '提升为管理员' : '降级为普通用户'
  if (!confirm(`确认将 ${user.username} ${action}？`)) return
  try {
    await userApi.updateRole(user.id, newRole)
    await fetchUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || '操作失败')
  }
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(fetchUsers)
</script>

<template>
  <div class="admin-users">
    <div class="page-header">
      <h1>用户管理</h1>
      <button class="btn-primary" @click="openCreate">创建用户</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>角色</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="cell-light">{{ user.id }}</td>
            <td class="cell-name">{{ user.username }}</td>
            <td>
              <span
                class="role-badge"
                :class="user.role === 'admin' ? 'role-admin' : 'role-user'"
              >
                {{ user.role === 'admin' ? '管理员' : '普通用户' }}
              </span>
            </td>
            <td class="cell-light">{{ formatDate(user.created_at) }}</td>
            <td>
              <button
                v-if="user.id !== authStore.user?.id"
                class="btn-action"
                @click="toggleRole(user)"
              >
                {{ user.role === 'admin' ? '降级为用户' : '提升为管理员' }}
              </button>
              <span v-else class="cell-light">当前用户</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create User Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <h2>创建用户</h2>
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="form.username" required placeholder="请输入用户名" />
          </div>
          <div class="form-group">
            <label>初始密码</label>
            <input v-model="form.password" type="password" required placeholder="请设置初始密码" />
          </div>
          <div class="form-group">
            <label>角色</label>
            <select v-model="form.role">
              <option value="user">普通用户</option>
              <option value="admin">管理员</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showModal = false">取消</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-users {
  padding: 8px 0;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
}

.table-wrapper {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 16px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-bg-secondary);
}

td {
  padding: 14px 16px;
  font-size: 14px;
  color: var(--color-text);
  border-bottom: 1px solid var(--color-border);
}

tr:last-child td {
  border-bottom: none;
}

.cell-name {
  font-weight: 500;
}

.cell-light {
  color: var(--color-text-tertiary);
  font-size: 13px;
}

.role-badge {
  font-size: 12px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 6px;
}

.role-admin {
  color: var(--color-primary);
  background: rgba(0, 122, 255, 0.1);
}

.role-user {
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
}

.btn-action {
  font-size: 13px;
  color: var(--color-primary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: rgba(0, 122, 255, 0.08);
}

.btn-primary {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  background: var(--color-primary);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #0066d6;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal-content {
  background: var(--color-bg);
  border-radius: 16px;
  padding: 32px;
  width: 90%;
  max-width: 440px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.modal-content h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 14px;
  font-size: 15px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  background: var(--color-bg-secondary);
  color: var(--color-text);
  outline: none;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.12);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-cancel {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: var(--color-border);
}
</style>
