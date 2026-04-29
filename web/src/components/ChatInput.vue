<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ send: [text: string] }>()
defineProps<{ disabled: boolean }>()

const text = ref('')
const inputRef = ref<HTMLTextAreaElement>()

function submit() {
  const val = text.value.trim()
  if (!val) return
  emit('send', val)
  text.value = ''
  inputRef.value?.focus()
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submit()
  }
}
</script>

<template>
  <div class="border-t border-gray-200 p-4 bg-white shrink-0">
    <div class="max-w-4xl mx-auto flex gap-3">
      <textarea
        ref="inputRef"
        v-model="text"
        :disabled="disabled"
        rows="1"
        placeholder="输入消息..."
        class="flex-1 resize-none rounded-xl bg-gray-100 px-4 py-3 text-sm text-gray-900 placeholder-gray-400 border border-gray-300 focus:outline-none focus:border-indigo-500 disabled:opacity-50"
        @keydown="onKeydown"
      />
      <button
        :disabled="disabled || !text.trim()"
        class="shrink-0 self-end rounded-xl bg-indigo-500 px-5 py-3 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        @click="submit"
      >
        发送
      </button>
    </div>
  </div>
</template>
