<script lang="ts">
  import type { TutorialIcon } from '$lib/data/tutorials';

  let {
    name,
    className = 'h-5 w-5'
  }: {
    name?: TutorialIcon;
    className?: string;
  } = $props();
</script>

{#if name === 'rocket'}
  <span class={className}>🚀</span>
{:else if name === 'settings'}
  <span class={className}>⚙️</span>
{:else if name === 'database'}
  <span class={className}>🗄️</span>
{:else if name === 'shield'}
  <span class={className}>🛡️</span>
{:else if name === 'key'}
  <span class={className}>🔑</span>
{:else if name === 'sync'}
  <span class={className}>🔄</span>
{:else if name === 'sparkles'}
  <span class={className}>✨</span>
{:else if name === 'server'}
  <span class={className}>🖥️</span>
{:else if name === 'bug'}
  <span class={className}>🐞</span>
{:else if name === 'wrench'}
  <span class={className}>🔧</span>
{:else if name === 'book'}
  <span class={className}>📘</span>
{:else if name === 'search'}
  <span class={className}>🔎</span>
{:else if name === 'folder'}
  <span class={className}>📁</span>
{:else}
  <span class={className}>•</span>
{/if}