<script lang="ts">
  import type { TutorialAccordionItem } from '$lib/data/tutorials';
  import TutorialCallout from './TutorialCallout.svelte';
  import TutorialCodeBlock from './TutorialCodeBlock.svelte';

  let {
    item
  }: {
    item: TutorialAccordionItem;
  } = $props();

  let open = $state(false);
</script>

<section class="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
  <button
    type="button"
    on:click={() => (open = !open)}
    class="flex w-full items-center justify-between gap-4 px-5 py-4 text-left"
  >
    <h3 class="text-base font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
      {item.title}
    </h3>
    <span class="text-zinc-500">{open ? '−' : '+'}</span>
  </button>

  {#if open}
    <div class="border-t border-zinc-200 px-5 py-5 dark:border-zinc-800">
      {#if item.content?.length}
        <div class="space-y-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
          {#each item.content as paragraph}
            <p>{paragraph}</p>
          {/each}
        </div>
      {/if}

      {#if item.callouts?.length}
        <div class="mt-4 space-y-4">
          {#each item.callouts as callout}
            <TutorialCallout {callout} />
          {/each}
        </div>
      {/if}

      {#if item.codeBlocks?.length}
        <div class="mt-4 space-y-4">
          {#each item.codeBlocks as block}
            <TutorialCodeBlock {block} />
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</section>