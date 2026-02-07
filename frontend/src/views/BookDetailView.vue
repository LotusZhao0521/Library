<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { Book, BorrowRecord } from '@/types'
import { bookApi } from '@/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const book = ref<Book | null>(null)
const records = ref<BorrowRecord[]>([])
const loading = ref(true)
const actionLoading = ref(false)
const bookId = Number(route.params.id)

async function fetchData() {
  loading.value = true
  try {
    const [bookRes, recordsRes] = await Promise.all([
      bookApi.get(bookId),
      bookApi.getRecords(bookId),
    ])
    book.value = bookRes.data
    records.value = recordsRes.data
  } finally {
    loading.value = false
  }
}

async function handleBorrow() {
  actionLoading.value = true
  try {
    await bookApi.borrow(bookId)
    await fetchData()
  } catch (e: any) {
    alert(e.response?.data?.detail || '借阅失败')
  } finally {
    actionLoading.value = false
  }
}

async function handleReturn() {
  actionLoading.value = true
  try {
    await bookApi.return(bookId)
    await fetchData()
  } catch (e: any) {
    alert(e.response?.data?.detail || '归还失败')
  } finally {
    actionLoading.value = false
  }
}

function isMyActiveBorrow(): boolean {
  return records.value.some(
    (r) => r.user_id === authStore.user?.id && !r.return_time,
  )
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(fetchData)
</script>

<template>
  <div class="book-detail">
    <button class="btn-back" @click="router.back()">← 返回</button>

    <div v-if="loading" class="loading">加载中...</div>

    <template v-else-if="book">
      <div class="detail-card">
        <div class="detail-header">
          <div class="detail-no">{{ book.book_no }}</div>
          <span
            class="detail-status"
            :class="book.status === 'available' ? 'status-available' : 'status-borrowed'"
          >
            {{ book.status === 'available' ? '可借阅' : '已借出' }}
          </span>
        </div>
        <h1 class="detail-title">{{ book.title }}</h1>
        <div class="detail-meta">
          <p><span class="label">作者</span>{{ book.author }}</p>
          <p v-if="book.isbn"><span class="label">ISBN</span>{{ book.isbn }}</p>
          <p v-if="book.publisher"><span class="label">出版社</span>{{ book.publisher }}</p>
        </div>
        <div class="detail-actions">
          <button
            v-if="book.status === 'available'"
            class="btn-primary"
            :disabled="actionLoading"
            @click="handleBorrow"
          >
            {{ actionLoading ? '处理中...' : '借阅此书' }}
          </button>
          <button
            v-else-if="isMyActiveBorrow()"
            class="btn-secondary"
            :disabled="actionLoading"
            @click="handleReturn"
          >
            {{ actionLoading ? '处理中...' : '归还此书' }}
          </button>
          <span v-else class="borrowed-hint">此书已被他人借出</span>
        </div>
      </div>

      <div v-if="records.length > 0" class="records-section">
        <h2>借阅记录</h2>
        <div class="records-list">
          <div v-for="record in records" :key="record.id" class="record-item">
            <div class="record-info">
              <span class="record-user">{{ record.user.username }}</span>
              <span class="record-time">{{ formatDate(record.borrow_time) }}</span>
              <span v-if="record.return_time" class="record-return">
                归还于 {{ formatDate(record.return_time) }}
              </span>
              <span v-else class="record-active">借阅中</span>
            </div>
            <div v-if="record.note" class="record-note">
              <p class="note-label">阅读心得</p>
              <p class="note-content">{{ record.note }}</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.book-detail {
  padding: 8px 0;
}

.btn-back {
  font-size: 14px;
  color: var(--color-primary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 0;
  margin-bottom: 24px;
}

.btn-back:hover {
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
}

.detail-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.detail-no {
  font-size: 13px;
  color: var(--color-text-tertiary);
  font-weight: 500;
}

.detail-status {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 6px;
}

.status-available {
  color: #34c759;
  background: rgba(52, 199, 89, 0.1);
}

.status-borrowed {
  color: #ff9500;
  background: rgba(255, 149, 0, 0.1);
}

.detail-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 20px;
}

.detail-meta p {
  font-size: 15px;
  color: var(--color-text);
  margin: 0 0 8px;
}

.detail-meta .label {
  color: var(--color-text-secondary);
  margin-right: 12px;
  min-width: 50px;
  display: inline-block;
}

.detail-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}

.btn-primary {
  padding: 10px 24px;
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

.btn-secondary {
  padding: 10px 24px;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-primary);
  background: rgba(0, 122, 255, 0.1);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(0, 122, 255, 0.16);
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.borrowed-hint {
  font-size: 14px;
  color: var(--color-text-tertiary);
}

.records-section h2 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 16px;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 16px 20px;
}

.record-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.record-user {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text);
}

.record-time {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

.record-return {
  font-size: 13px;
  color: #34c759;
}

.record-active {
  font-size: 12px;
  font-weight: 500;
  color: #ff9500;
  background: rgba(255, 149, 0, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
}

.record-note {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.note-label {
  font-size: 12px;
  color: var(--color-text-tertiary);
  margin: 0 0 4px;
}

.note-content {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}
</style>
