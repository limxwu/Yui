export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
}

export interface ChatRequest {
  message: string
  session_id: string
  use_rag: boolean
}
