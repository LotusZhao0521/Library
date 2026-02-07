<script setup lang="ts">
import { ref } from 'vue'
import { userApi } from '@/api'

const oldPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  message.value = ''

  if (newPassword.value !== confirmPassword.value) {
    error.value = '两次输入的新密码不一致'
    return
  }

  if (newPassword.value.length < 4) {
    error.value = '新密码长度不能少于4位'
    return
  }

  loading.value = true
  try {
    await userApi.changePassword(oldPassword.value, newPassword.value)
    message.value = '密码修改成功'
    oldPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail || '修改失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="change-password">
    <h1>修改密码</h1>
    <div class="form-card">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>当前密码</label>
          <input v-model="oldPassword" type="password" required />
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input v-model="newPassword" type="password" required />
        </div>
        <div class="form-group">
          <label>确认新密码</label>
          <input v-model="confirmPassword" type="password" required />
        </div>
        <div v-if="error" class="msg error">{{ error }}</div>
        <div v-if="message" class="msg success">{{ message }}</div>
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '提交中...' : '修改密码' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.change-password h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 32px;
}

.form-card {
  max-width: 420px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 32px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.form-group input {
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

.form-group input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.12);
}

.msg {
  font-size: 13px;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 16px;
  text-align: center;
}

.error {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.08);
}

.success {
  color: #34c759;
  background: rgba(52, 199, 89, 0.08);
}

.btn-primary {
  width: 100%;
  padding: 10px;
  font-size: 15px;
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
</style>
