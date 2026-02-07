<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { BorrowRecord } from '@/types'
import { borrowApi } from '@/api'

const records = ref<BorrowRecord[]>([])
const loading = ref(true)
const editingId = ref<number | null>(null)
const editNote = ref('')
const saving = ref(false)

async function fetchRecords() {
  loading.value = true
  try {
    const { data } = await borrowApi.listMine()
    records.value = data
  } finally {
    loading.value = false
  }
}

function startEdit(record: BorrowRecord) {
  editingId.value = record.id
  editNote.value = record.note || ''
}

function cancelEdit() {
  editingId.value = null
  editNote.value = ''
}

async function saveNote(recordId: number) {
  saving.value = true
  try {
    await borrowApi.updateNote(recordId, editNote.value)
    await fetchRecords()
    editingId.value = null
  } catch (e: any) {
    alert(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(fetchRecords)
</script>

<template>
  <div class="my-borrows">
    <h1>我的借阅</h1>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="records.length === 0" class="empty">
      <p>暂无借阅记录</p>
    </div>

    <div v-else class="records-list">
      <div v-for="record in records" :key="record.id" class="record-card">
        <div class="record-header">
          <div>
            <h3 class="record-book-title">{{ record.book.title }}</h3>
            <p class="record-book-author">{{ record.book.author }}</p>
          </div>
          <span
            class="record-status"
            :class="record.return_time ? 'status-returned' : 'status-active'"
          >
            {{ record.return_time ? '已归还' : '借阅中' }}
          </span>
        </div>
        <div class="record-dates">
          <span>借阅: {{ formatDate(record.borrow_time) }}</span>
          <span v-if="record.return_time">归还: {{ formatDate(record.return_time) }}</span>
        </div>
        <div class="record-note-section">
          <div v-if="editingId === record.id" class="note-editor">
            <textarea
              v-model="editNote"
              placeholder="写下你的阅读心得..."
              rows="3"
            ></textarea>
            <div class="note-actions">
              <button class="btn-sm btn-primary-sm" :disabled="saving" @click="saveNote(record.id)">
                {{ saving ? '保存中...' : '保存' }}
              </button>
              <button class="btn-sm btn-cancel" @click="cancelEdit">取消</button>
            </div>
          </div>
          <div v-else class="note-display">
            <p v-if="record.note" class="note-content">{{ record.note }}</p>
            <button class="btn-note" @click="startEdit(record)">
              {{ record.note ? '编辑心得' : '添加阅读心得' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-borrows h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 32px;
}

.loading,
.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
  font-size: 15px;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.record-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 24px;
}

.record-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.record-book-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 2px;
}

.record-book-author {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.record-status {
  font-size: 12px;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 6px;
  white-space: nowrap;
}

.status-active {
  color: #ff9500;
  background: rgba(255, 149, 0, 0.1);
}

.status-returned {
  color: #34c759;
  background: rgba(52, 199, 89, 0.1);
}

.record-dates {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: var(--color-text-tertiary);
  margin-bottom: 16px;
}

.record-note-section {
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.note-editor textarea {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  font-family: inherit;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  background: var(--color-bg-secondary);
  color: var(--color-text);
  outline: none;
  resize: vertical;
  box-sizing: border-box;
  transition: border-color 0.2s ease;
}

.note-editor textarea:focus {
  border-color: var(--color-primary);
}

.note-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.btn-sm {
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary-sm {
  color: white;
  background: var(--color-primary);
}

.btn-primary-sm:hover:not(:disabled) {
  background: #0066d6;
}

.btn-primary-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  color: var(--color-text-secondary);
  background: var(--color-bg-secondary);
}

.btn-cancel:hover {
  background: var(--color-border);
}

.note-content {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 12px;
  line-height: 1.6;
}

.btn-note {
  font-size: 13px;
  color: var(--color-primary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.btn-note:hover {
  text-decoration: underline;
}
</style>
