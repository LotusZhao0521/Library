export interface User {
  id: number
  username: string
  role: 'admin' | 'user'
  created_at: string
}

export interface Book {
  id: number
  book_no: string
  title: string
  author: string
  isbn: string | null
  publisher: string | null
  status: 'available' | 'borrowed'
  created_at: string
}

export interface BorrowRecord {
  id: number
  book_id: number
  user_id: number
  borrow_time: string
  return_time: string | null
  note: string | null
  book: Book
  user: User
}

export interface Token {
  access_token: string
  token_type: string
}
