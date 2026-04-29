import { ref, reactive } from 'vue'
import type { Message } from '../types'
import { streamChat, clearSession } from '../api'

function genId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 9)
}

function getSessionId(): string {
  const key = 'yui_session_id'
  const stored = localStorage.getItem(key)
  if (stored) return stored
  const id = genId()
  localStorage.setItem(key, id)
  return id
}

export function useChat() {
  const messages = ref<Message[]>([])
  const isLoading = ref(false)
  const useRag = ref(true)
  const sessionId = ref(getSessionId())

  function resetSession() {
    sessionId.value = genId()
    localStorage.setItem('yui_session_id', sessionId.value)
  }

  async function sendMessage(text: string) {
    if (!text.trim() || isLoading.value) return

    messages.value.push({ id: genId(), role: 'user', content: text })

    const assistantMsg = reactive<Message>({ id: genId(), role: 'assistant', content: '' })
    messages.value.push(assistantMsg)

    isLoading.value = true

    try {
      for await (const chunk of streamChat(text, sessionId.value, useRag.value)) {
        assistantMsg.content += chunk
      }
    } catch (e: unknown) {
      assistantMsg.content = `错误: ${e instanceof Error ? e.message : '请求失败'}`
    } finally {
      isLoading.value = false
    }
  }

  async function clearChat() {
    try {
      await clearSession(sessionId.value)
    } catch { /* ignore */ }
    messages.value = []
    resetSession()
  }

  return { messages, isLoading, useRag, sessionId, sendMessage, clearChat }
}
