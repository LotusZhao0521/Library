<script setup lang="ts">
import { onMounted, ref } from 'vue'
import type { Book } from '@/types'
import { bookApi } from '@/api'

const books = ref<Book[]>([])
const loading = ref(true)
const showModal = ref(false)
const editingBook = ref<Book | null>(null)
const saving = ref(false)

const form = ref({
  book_no: '',
  title: '',
  author: '',
  isbn: '',
  publisher: '',
})

async function fetchBooks() {
  loading.value = true
  try {
    const { data } = await bookApi.list()
    books.value = data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingBook.value = null
  form.value = { book_no: '', title: '', author: '', isbn: '', publisher: '' }
  showModal.value = true
}

function openEdit(book: Book) {
  editingBook.value = book
  form.value = {
    book_no: book.book_no,
    title: book.title,
    author: book.author,
    isbn: book.isbn || '',
    publisher: book.publisher || '',
  }
  showModal.value = true
}

async function handleSave() {
  saving.value = true
  try {
    const data = {
      ...form.value,
      isbn: form.value.isbn || undefined,
      publisher: form.value.publisher || undefined,
    }
    if (editingBook.value) {
      await bookApi.update(editingBook.value.id, data)
    } else {
      await bookApi.create(data as any)
    }
    showModal.value = false
    await fetchBooks()
  } catch (e: any) {
    alert(e.response?.data?.detail || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(book: Book) {
  if (!confirm(`确认删除《${book.title}》？`)) return
  try {
    await bookApi.delete(book.id)
    await fetchBooks()
  } catch (e: any) {
    alert(e.response?.data?.detail || '删除失败')
  }
}

onMounted(fetchBooks)
</script>

<template>
  <div class="admin-books">
    <div class="page-header">
      <h1>图书管理</h1>
      <button class="btn-primary" @click="openCreate">添加图书</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>编号</th>
            <th>书名</th>
            <th>作者</th>
            <th>ISBN</th>
            <th>出版社</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td class="cell-no">{{ book.book_no }}</td>
            <td class="cell-title">{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td class="cell-light">{{ book.isbn || '-' }}</td>
            <td class="cell-light">{{ book.publisher || '-' }}</td>
            <td>
              <span
                class="status-badge"
                :class="book.status === 'available' ? 'status-available' : 'status-borrowed'"
              >
                {{ book.status === 'available' ? '可借阅' : '已借出' }}
              </span>
            </td>
            <td class="cell-actions">
              <button class="btn-action" @click="openEdit(book)">编辑</button>
              <button class="btn-action btn-danger" @click="handleDelete(book)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <h2>{{ editingBook ? '编辑图书' : '添加图书' }}</h2>
        <form @submit.prevent="handleSave">
          <div class="form-group">
            <label>图书编号</label>
            <input v-model="form.book_no" required placeholder="如 B001" />
          </div>
          <div class="form-group">
            <label>书名</label>
            <input v-model="form.title" required placeholder="请输入书名" />
          </div>
          <div class="form-group">
            <label>作者</label>
            <input v-model="form.author" required placeholder="请输入作者" />
          </div>
          <div class="form-group">
            <label>ISBN (可选)</label>
            <input v-model="form.isbn" placeholder="请输入 ISBN" />
          </div>
          <div class="form-group">
            <label>出版社 (可选)</label>
            <input v-model="form.publisher" placeholder="请输入出版社" />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showModal = false">取消</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-books {
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

.cell-no {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.cell-title {
  font-weight: 500;
}

.cell-light {
  color: var(--color-text-tertiary);
}

.status-badge {
  font-size: 12px;
  font-weight: 500;
  padding: 3px 8px;
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

.cell-actions {
  display: flex;
  gap: 8px;
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

.btn-danger {
  color: #ff3b30;
}

.btn-danger:hover {
  background: rgba(255, 59, 48, 0.08);
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
