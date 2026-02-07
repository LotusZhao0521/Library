<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { Book } from '@/types'
import { bookApi } from '@/api'

const router = useRouter()
const books = ref<Book[]>([])
const loading = ref(true)
const searchQuery = ref('')

const filteredBooks = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (!q) return books.value
  return books.value.filter(
    (b) =>
      b.title.toLowerCase().includes(q) ||
      b.author.toLowerCase().includes(q) ||
      b.book_no.toLowerCase().includes(q),
  )
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

function goToBook(id: number) {
  router.push(`/books/${id}`)
}

onMounted(fetchBooks)
</script>

<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>图书列表</h1>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索书名、作者或编号..."
        />
      </div>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="filteredBooks.length === 0" class="empty">
      <p>{{ searchQuery ? '未找到匹配的图书' : '暂无图书' }}</p>
    </div>

    <div v-else class="book-grid">
      <div
        v-for="book in filteredBooks"
        :key="book.id"
        class="book-card"
        @click="goToBook(book.id)"
      >
        <div class="book-no">{{ book.book_no }}</div>
        <h3 class="book-title">{{ book.title }}</h3>
        <p class="book-author">{{ book.author }}</p>
        <div class="book-footer">
          <span
            class="book-status"
            :class="book.status === 'available' ? 'status-available' : 'status-borrowed'"
          >
            {{ book.status === 'available' ? '可借阅' : '已借出' }}
          </span>
          <span v-if="book.publisher" class="book-publisher">{{ book.publisher }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  padding: 8px 0;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.search-bar input {
  padding: 10px 16px;
  font-size: 14px;
  border: 1px solid var(--color-border);
  border-radius: 10px;
  background: var(--color-bg);
  color: var(--color-text);
  outline: none;
  width: 280px;
  transition: all 0.2s ease;
}

.search-bar input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.12);
}

.loading,
.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--color-text-secondary);
  font-size: 15px;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.book-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.book-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border-color: transparent;
}

.book-no {
  font-size: 12px;
  color: var(--color-text-tertiary);
  font-weight: 500;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.book-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 4px;
  line-height: 1.4;
}

.book-author {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 16px;
}

.book-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.book-status {
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

.book-publisher {
  font-size: 12px;
  color: var(--color-text-tertiary);
}
</style>
