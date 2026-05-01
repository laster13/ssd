<script lang="ts">
  import type { TutorialTabItem } from '$lib/data/tutorials';
  import TutorialCallout from './TutorialCallout.svelte';
  import TutorialCodeBlock from './TutorialCodeBlock.svelte';

  let {
    tabs
  }: {
    tabs: TutorialTabItem[];
  } = $props();

  let activeIndex = $state(0);

  function linkify(text: string) {
    const escaped = text
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');

    return escaped.replace(
      /(https?:\/\/[^\s<]+)/g,
      '<a href="$1" target="_blank" rel="noreferrer" class="underline underline-offset-4 hover:no-underline">$1</a>'
    );
  }
</script>

<section class="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
  <div class="overflow-x-auto border-b border-zinc-200 px-3 py-3 dark:border-zinc-800 sm:px-4 sm:py-4">
    <div class="flex min-w-max gap-2">
      {#each tabs as tab, index}
        <button
          type="button"
          on:click={() => (activeIndex = index)}
          class={`whitespace-nowrap rounded-xl px-3 py-2 text-sm font-medium transition ${
            activeIndex === index
              ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900'
              : 'bg-zinc-100 text-zinc-600 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300'
          }`}
        >
          {tab.label}
        </button>
      {/each}
    </div>
  </div>

  <div class="px-4 py-4 sm:px-5 sm:py-5">
    {#if tabs[activeIndex]?.content?.length}
      <div class="space-y-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
        {#each tabs[activeIndex].content as paragraph}
          <p>{@html linkify(paragraph)}</p>
        {/each}
      </div>
    {/if}

    {#if tabs[activeIndex]?.callouts?.length}
      <div class="mt-4 space-y-4">
        {#each tabs[activeIndex].callouts as callout}
          <TutorialCallout {callout} />
        {/each}
      </div>
    {/if}

    {#if tabs[activeIndex]?.codeBlocks?.length}
      <div class="mt-4 space-y-4">
        {#each tabs[activeIndex].codeBlocks as block}
          <TutorialCodeBlock {block} />
        {/each}
      </div>
    {/if}
  </div>
</section>