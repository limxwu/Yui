<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import ChatMessage from './components/ChatMessage.vue'
import ChatInput from './components/ChatInput.vue'
import Sidebar from './components/Sidebar.vue'
import { useChat } from './composables/useChat'

const { messages, isLoading, useRag, sessionId, sendMessage, clearChat } = useChat()
const messagesRef = ref<HTMLElement>()

watch(
  () => messages.value.length,
  async () => {
    await nextTick()
    messagesRef.value?.lastElementChild?.scrollIntoView({ behavior: 'smooth' })
  },
)
</script>

<template>
  <div class="flex h-screen bg-white text-gray-900">
    <Sidebar
      :use-rag="useRag"
      :session-id="sessionId"
      @update:use-rag="useRag = $event"
      @clear="clearChat"
    />

    <div class="flex-1 flex flex-col min-w-0">
      <header class="border-b border-gray-200 px-6 py-3 shrink-0">
        <h1 class="text-lg font-semibold">Yui — AI 对话助手</h1>
      </header>

      <div
        ref="messagesRef"
        class="flex-1 overflow-y-auto px-4 py-6 space-y-4 max-w-5xl w-full mx-auto"
      >
        <p
          v-if="messages.length === 0"
          class="text-center text-gray-400 mt-24 text-sm"
        >
          开始和 Yui 对话吧
        </p>

        <ChatMessage v-for="msg in messages" :key="msg.id" :message="msg" />

        <div v-if="isLoading" class="flex justify-center pt-2">
          <span class="text-gray-400 text-sm animate-pulse">思考中...</span>
        </div>
      </div>

      <ChatInput :disabled="isLoading" @send="sendMessage" />
    </div>
  </div>
</template>
