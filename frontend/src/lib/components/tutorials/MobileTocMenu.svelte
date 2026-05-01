<script lang="ts">
  import type { TocItem } from '$lib/data/tutorials';

  let {
    items
  }: {
    items: TocItem[];
  } = $props();

  let open = $state(false);
</script>

{#if items.length}
  <div class="xl:hidden">
    <button
      type="button"
      onclick={() => (open = true)}
      class="flex w-full items-center justify-between rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-left text-sm font-medium text-zinc-800 shadow-sm transition hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100"
    >
      <span>Sommaire de la page</span>
      <span class="text-zinc-500">≡</span>
    </button>

    {#if open}
      <div class="fixed inset-0 z-[90] bg-black/40 backdrop-blur-sm" onclick={() => (open = false)}>
        <div class="flex min-h-full items-end justify-center p-2 sm:p-4">
          <div
            class="w-full max-w-xl overflow-hidden rounded-t-3xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-800 dark:bg-zinc-900 sm:rounded-3xl"
            onclick={(event) => event.stopPropagation()}
          >
            <div class="flex items-center justify-between border-b border-zinc-200 px-4 py-4 dark:border-zinc-800">
              <h2 class="text-base font-semibold text-zinc-900 dark:text-zinc-100">
                Sur cette page
              </h2>

              <button
                type="button"
                onclick={() => (open = false)}
                class="rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
              >
                Fermer
              </button>
            </div>

            <div class="max-h-[70vh] overflow-y-auto p-4">
              <ul class="space-y-2">
                {#each items as item}
                  <li>
                    <a
                      href={`#${item.id}`}
                      onclick={() => (open = false)}
                      class={`block rounded-xl px-3 py-2 text-sm text-zinc-600 transition hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-100 ${
                        item.level === 3 ? 'ml-4' : ''
                      }`}
                    >
                      {item.label}
                    </a>
                  </li>
                {/each}
              </ul>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
{/if}