<script lang="ts">
  import type { TocItem } from '$lib/data/tutorials';

  let {
    items
  }: {
    items: TocItem[];
  } = $props();
</script>

{#if items.length}
  <aside class="sticky top-24 rounded-3xl border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-5">
    <h2 class="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500 sm:text-sm">
      Sur cette page
    </h2>

    <ul class="mt-4 space-y-2">
      {#each items as item}
        <li>
          <a
            href={`#${item.id}`}
            class={`block rounded-xl px-3 py-2 text-sm leading-5 text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-100 ${
              item.level === 3 ? 'ml-4' : ''
            }`}
          >
            {item.label}
          </a>
        </li>
      {/each}
    </ul>
  </aside>
{/if}