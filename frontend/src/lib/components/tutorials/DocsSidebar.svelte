<script lang="ts">
  import type { DocsNavGroup } from '$lib/data/tutorials';

  let {
    groups,
    currentSlug
  }: {
    groups: DocsNavGroup[];
    currentSlug?: string;
  } = $props();
</script>

<aside class="rounded-3xl border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-5">
  <h2 class="text-xs font-semibold uppercase tracking-[0.16em] text-zinc-500 sm:text-sm">
    Documentation
  </h2>

  <div class="mt-4 space-y-4 sm:space-y-5">
    {#each groups as group}
      <section>
        <h3 class="text-sm font-semibold text-zinc-900 dark:text-zinc-100">{group.name}</h3>

        <div class="mt-3 space-y-4">
          {#each group.categories as category}
            <div>
              <h4 class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-500 sm:text-xs">
                {category.name}
              </h4>

              <ul class="mt-2 space-y-1">
                {#each category.items as item}
                  <li>
                    <a
                      href={`/tutos/${item.slug}`}
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
</aside>