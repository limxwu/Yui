<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js/lib/core'
import python from 'highlight.js/lib/languages/python'
import javascript from 'highlight.js/lib/languages/javascript'
import typescript from 'highlight.js/lib/languages/typescript'
import bash from 'highlight.js/lib/languages/bash'
import json from 'highlight.js/lib/languages/json'
import yaml from 'highlight.js/lib/languages/yaml'
import sql from 'highlight.js/lib/languages/sql'
import xml from 'highlight.js/lib/languages/xml'
import type { Message } from '../types'

hljs.registerLanguage('python', python)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('bash', bash)
hljs.registerLanguage('json', json)
hljs.registerLanguage('yaml', yaml)
hljs.registerLanguage('sql', sql)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('js', javascript)
hljs.registerLanguage('ts', typescript)

const props = defineProps<{ message: Message }>()

const rendered = computed(() => {
  if (props.message.role === 'user') return ''
  const html = marked.parse(props.message.content, { async: false }) as string
  return highlightCodeBlocks(html)
})

// 确保在组件挂载后重新应用高亮样式
onMounted(() => {
  // 可以在这里添加额外的初始化逻辑，如果需要的话
})

const entities: Record<string, string> = {
  '&amp;': '&',
  '&lt;': '<',
  '&gt;': '>',
  '&quot;': '"',
  '&#39;': "'",
  '&#x27;': "'",
  '&#x60;': '`',
}

function decodeEntities(text: string): string {
  return text.replace(/&amp;|&lt;|&gt;|&quot;|&#39;|&#x27;|&#x60;/g, (m) => entities[m])
}

function highlightCodeBlocks(html: string): string {
  return html.replace(
    /<pre><code(?:\s+class="language-(\w+)")?>([\s\S]*?)<\/code><\/pre>/g,
    (_, lang, code) => {
      const decoded = decodeEntities(code)
      let highlighted = ''
      
      if (lang && hljs.getLanguage(lang)) {
        try {
          highlighted = hljs.highlight(decoded, { language: lang }).value
        } catch (e) {
          // 如果特定语言高亮失败，尝试自动检测或使用纯文本
          try {
            highlighted = hljs.highlightAuto(decoded).value
          } catch (e2) {
            // 最终回退到转义后的纯文本
            highlighted = decoded
              .replace(/&/g, '&amp;')
              .replace(/</g, '&lt;')
              .replace(/>/g, '&gt;')
          }
        }
      } else {
        // 没有指定语言或语言不支持时，尝试自动检测
        try {
          const result = hljs.highlightAuto(decoded)
          highlighted = result.value
          lang = result.language || ''
        } catch (e) {
          // 最终回退到转义后的纯文本
          highlighted = decoded
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
        }
      }
      
      const className = lang ? `hljs language-${lang}` : 'hljs'
      return `<pre><code class="${className}">${highlighted}</code></pre>`
    },
  )
}
</script>

<template>
  <div :class="[
    'flex',
    message.role === 'user' ? 'justify-end' : 'justify-start'
  ]">
    <div :class="[
      'max-w-[75%] rounded-2xl px-4 py-2.5 break-words',
      message.role === 'user'
        ? 'bg-indigo-500 text-white rounded-br-md'
        : 'bg-gray-100 text-gray-900 rounded-bl-md'
    ]">
      <template v-if="message.role === 'user'">{{ message.content }}</template>
      <div v-else class="markdown-body" v-html="rendered" />
    </div>
  </div>
</template>
