<script lang="ts">
  import type { DocsNavGroup } from '$lib/data/tutorials';

  let {
    groups,
    currentSlug,
    homeHref = '/',
    docsHref = '/tutos'
  }: {
    groups: DocsNavGroup[];
    currentSlug?: string;
    homeHref?: string;
    docsHref?: string;
  } = $props();

  let open = $state(false);
</script>

<div class="xl:hidden">
  <button
    type="button"
    onclick={() => (open = true)}
    class="flex w-full items-center justify-between rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-left text-sm font-medium text-zinc-800 shadow-sm transition hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100"
  >
    <span>Parcourir la documentation</span>
    <span class="text-zinc-500">☰</span>
  </button>

  {#if open}
    <div class="fixed inset-0 z-[90] bg-black/40 backdrop-blur-sm" onclick={() => (open = false)}>
      <div class="flex min-h-full items-end justify-center p-2 sm:p-4">
        <div
          class="w-full max-w-2xl overflow-hidden rounded-t-3xl border border-zinc-200 bg-white shadow-2xl dark:border-zinc-800 dark:bg-zinc-900 sm:rounded-3xl"
          onclick={(event) => event.stopPropagation()}
        >
          <div class="flex items-center justify-between border-b border-zinc-200 px-4 py-4 dark:border-zinc-800">
            <h2 class="text-base font-semibold text-zinc-900 dark:text-zinc-100">
              Documentation
            </h2>

            <button
              type="button"
              onclick={() => (open = false)}
              class="rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
            >
              Fermer
            </button>
          </div>

          <div class="max-h-[78vh] overflow-y-auto p-4">
            <div class="mb-4 flex flex-col gap-2">
              <a
                href={homeHref}
                onclick={() => (open = false)}
                class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm font-medium text-zinc-800 transition hover:bg-white dark:border-zinc-800 dark:bg-zinc-950/40 dark:text-zinc-100"
              >
                ← Retour à l’accueil
              </a>

              <a
                href={docsHref}
                onclick={() => (open = false)}
                class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm font-medium text-zinc-800 transition hover:bg-white dark:border-zinc-800 dark:bg-zinc-950/40 dark:text-zinc-100"
              >
                Voir toute la documentation
              </a>
            </div>

            <div class="space-y-5">
              {#each groups as group}
                <section>
                  <h3 class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{group.name}</h3>

                  <div class="mt-3 space-y-4">
                    {#each group.categories as category}
                      <div>
                        <h4 class="text-xs font-semibold uppercase tracking-[0.12em] text-zinc-500">
                          {category.name}
                        </h4>

                        <ul class="mt-2 space-y-1">
                          {#each category.items as item}
                            <li>
                              <a
                                href={`/tutos/${item.slug}`}
                                onclick={() => (open = false)}
                                aria-current={currentSlug === item.slug ? 'page' : undefined}
                                class={`block rounded-xl px-3 py-2 text-sm leading-5 transition ${
                                  currentSlug === item.slug
                                    ? 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900'
                                    : 'text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-300 dark:hover:bg-zinc-800 dark:hover:text-zinc-100'
                                }`}
                              >
                                {item.title}
                              </a>
                            </li>
                          {/each}
                        </ul>
                      </div>
                    {/each}
                  </div>
                </section>
              {/each}
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>