<script setup lang="ts">
import { ref } from 'vue'
import { uploadDocument } from '../api'

const props = defineProps<{
  useRag: boolean
  sessionId: string
}>()

const emit = defineEmits<{
  'update:useRag': [value: boolean]
  clear: []
}>()

const uploading = ref(false)
const uploadMsg = ref('')
const uploadMsgType = ref<'success' | 'error'>('success')

async function handleUpload(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploading.value = true
  uploadMsg.value = ''
  try {
    const msg = await uploadDocument(file)
    uploadMsg.value = msg
    uploadMsgType.value = 'success'
  } catch (err: unknown) {
    uploadMsg.value = err instanceof Error ? err.message : '上传失败'
    uploadMsgType.value = 'error'
  } finally {
    uploading.value = false
    input.value = ''
  }
}
</script>

<template>
  <aside class="w-64 lg:w-72 shrink-0 bg-gray-50 border-r border-gray-200 flex flex-col p-5 overflow-y-auto">
    <h2 class="text-lg font-semibold mb-6">设置</h2>

    <div class="mb-6">
      <label class="flex items-center gap-2.5 cursor-pointer select-none">
        <input
          type="checkbox"
          :checked="useRag"
          class="accent-indigo-500 w-4 h-4"
          @change="emit('update:useRag', ($event.target as HTMLInputElement).checked)"
        />
        <span class="text-sm text-gray-700">知识库检索 (RAG)</span>
      </label>
      <p class="text-xs text-gray-400 mt-1 ml-6">启用后从上传的文档中检索信息</p>
    </div>

    <div class="mb-6">
      <h3 class="text-sm font-medium text-gray-500 mb-2">文档上传</h3>
      <label
        class="flex items-center justify-center gap-2 rounded-lg border border-dashed border-gray-300 px-4 py-3 cursor-pointer hover:border-gray-400 transition-colors text-sm text-gray-500"
      >
        <span>选择文件</span>
        <input type="file" accept=".pdf,.docx,.doc,.txt" class="hidden" @change="handleUpload" />
      </label>
      <p v-if="uploadMsg" :class="[
        'text-xs mt-2',
        uploadMsgType === 'success' ? 'text-green-600' : 'text-red-600'
      ]">
        {{ uploadMsg }}
      </p>
    </div>

    <button
      class="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
      @click="emit('clear')"
    >
      清除对话
    </button>

    <p class="text-xs text-gray-400 mt-auto pt-6 select-all">
      Session: {{ sessionId.slice(0, 8) }}...
    </p>
  </aside>
</template>
