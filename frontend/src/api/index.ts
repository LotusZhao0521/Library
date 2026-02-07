import axios from 'axios'
import type { Book, BorrowRecord, Token, User } from '@/types'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: '/api/v1',
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

// Auth
export const authApi = {
  login: (username: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    return api.post<Token>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },
}

// Users
export const userApi = {
  getMe: () => api.get<User>('/users/me'),
  changePassword: (oldPassword: string, newPassword: string) =>
    api.put<User>('/users/me/password', {
      old_password: oldPassword,
      new_password: newPassword,
    }),
  create: (data: { username: string; password: string; role: string }) =>
    api.post<User>('/users/', data),
  list: () => api.get<User[]>('/users/'),
  updateRole: (userId: number, role: string) =>
    api.put<User>(`/users/${userId}/role`, { role }),
}

// Books
export const bookApi = {
  list: () => api.get<Book[]>('/books/'),
  get: (id: number) => api.get<Book>(`/books/${id}`),
  create: (data: {
    book_no: string
    title: string
    author: string
    isbn?: string
    publisher?: string
  }) => api.post<Book>('/books/', data),
  update: (id: number, data: Partial<Book>) => api.put<Book>(`/books/${id}`, data),
  delete: (id: number) => api.delete(`/books/${id}`),
  borrow: (id: number) => api.post<BorrowRecord>(`/books/${id}/borrow`),
  return: (id: number) => api.post<BorrowRecord>(`/books/${id}/return`),
  getRecords: (id: number) => api.get<BorrowRecord[]>(`/books/${id}/records`),
}

// Borrow Records
export const borrowApi = {
  listMine: () => api.get<BorrowRecord[]>('/borrow-records/'),
  updateNote: (recordId: number, note: string) =>
    api.put<BorrowRecord>(`/borrow-records/${recordId}/note`, { note }),
}

export default api
