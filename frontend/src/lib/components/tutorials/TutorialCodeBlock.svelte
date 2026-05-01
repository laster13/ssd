<script lang="ts">
  import type { TutorialCodeBlock } from '$lib/data/tutorials';

  let {
    block
  }: {
    block: TutorialCodeBlock;
  } = $props();

  let copied = $state(false);

  async function copyCode() {
    await navigator.clipboard.writeText(block.code);
    copied = true;
    setTimeout(() => {
      copied = false;
    }, 1500);
  }
</script>

<section class="rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
  <div class="flex flex-col gap-3 border-b border-zinc-200 px-4 py-4 dark:border-zinc-800 sm:flex-row sm:items-center sm:justify-between sm:px-5">
    <div class="min-w-0">
      {#if block.title}
        <h3 class="text-base font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
          {block.title}
        </h3>
      {/if}
      {#if block.language}
        <p class="mt-1 text-xs uppercase tracking-[0.14em] text-zinc-500">
          {block.language}
        </p>
      {/if}
    </div>

    <button
      type="button"
      on:click={copyCode}
      class="self-start rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-700 transition hover:bg-white dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
    >
      {copied ? 'Copié' : 'Copier'}
    </button>
  </div>

  <div class="overflow-x-auto rounded-b-3xl bg-zinc-950 p-4 text-sm text-zinc-100 sm:p-5">
    <pre class="min-w-max whitespace-pre font-mono">{block.code}</pre>
  </div>
</section>