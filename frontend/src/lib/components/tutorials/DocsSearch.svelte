<script lang="ts">
  import type { Tutorial } from '$lib/data/tutorials';

  let {
    tutorials
  }: {
    tutorials: Tutorial[];
  } = $props();

  let open = $state(false);
  let query = $state('');

  const results = $derived(
    tutorials.filter((tutorial) => {
      const q = query.trim().toLowerCase();
      if (!q) return true;

      return [
        tutorial.title,
        tutorial.description,
        tutorial.category,
        tutorial.group ?? '',
        ...(tutorial.tags ?? [])
      ]
        .join(' ')
        .toLowerCase()
        .includes(q);
    })
  );

  function handleKeydown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      open = true;
    }

    if (event.key === 'Escape') {
      open = false;
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<div>
  <button
    type="button"
    on:click={() => (open = true)}
    class="flex w-full items-center justify-between gap-3 rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-left text-sm text-zinc-500 shadow-sm transition hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300"
  >
    <span class="truncate">Rechercher dans la documentation…</span>
    <span class="hidden rounded-lg bg-zinc-100 px-2 py-1 text-xs dark:bg-zinc-800 sm:inline-block">Ctrl K</span>
  </button>

  {#if open}
    <div class="fixed inset-0 z-50 bg-black/40 p-3 backdrop-blur-sm sm:p-4" on:click={() => (open = false)}>
      <div
        class="mx-auto mt-8 max-w-2xl rounded-3xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-800 dark:bg-zinc-900 sm:mt-16"
        on:click|stopPropagation
      >
        <div class="border-b border-zinc-200 p-3 dark:border-zinc-800 sm:p-4">
          <input
            bind:value={query}
            placeholder="Titre, catégorie, tag…"
            class="w-full rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-base outline-none focus:border-zinc-400 dark:border-zinc-700 dark:bg-zinc-800"
          />
        </div>

        <div class="max-h-[70vh] overflow-y-auto p-3">
          {#if results.length}
            <div class="space-y-2">
              {#each results as tutorial}
                <a
                  href={`/tutos/${tutorial.slug}`}
                  class="block rounded-2xl border border-zinc-200 bg-zinc-50 p-4 transition hover:bg-white dark:border-zinc-800 dark:bg-zinc-950/40 dark:hover:bg-zinc-800"
                  on:click={() => (open = false)}
                >
                  <div class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                    {tutorial.title}
                  </div>
                  <div class="mt-1 text-xs text-zinc-500">
                    {tutorial.group ?? 'Guides'} · {tutorial.category}
                  </div>
                  <p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
                    {tutorial.description}
                  </p>
                </a>
              {/each}
            </div>
          {:else}
            <p class="p-4 text-sm text-zinc-500">Aucun résultat.</p>
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>