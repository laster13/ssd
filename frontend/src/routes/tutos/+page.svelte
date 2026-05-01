<script lang="ts">
  import DocsSearch from '$lib/components/tutorials/DocsSearch.svelte';
  import DocsSidebar from '$lib/components/tutorials/DocsSidebar.svelte';
  import TutorialBadge from '$lib/components/tutorials/TutorialBadge.svelte';
  import type { DocsNavGroup, Tutorial } from '$lib/data/tutorials';

  let {
    data
  }: {
    data: {
      tutorials: Tutorial[];
      docsNavGroups: DocsNavGroup[];
    };
  } = $props();
</script>
<svelte:head>
  <title>Documentation | SSD</title>
  <meta name="description" content="Documentation et tutoriels SSD." />
</svelte:head>

<section class="mx-auto max-w-7xl px-3 py-6 sm:px-6 sm:py-10 lg:px-8">
  <div class="grid gap-6 lg:grid-cols-[280px_1fr] lg:gap-8">
    <div class="space-y-4 sm:space-y-6">
      <a
        href="/"
        class="flex w-full items-center rounded-2xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-500 shadow-sm transition hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-300 dark:hover:text-zinc-100"
      >
        ← Retour à l’accueil
      </a>

  <DocsSearch tutorials={data.tutorials} />
  <DocsSidebar groups={data.docsNavGroups} />
</div>
    <div class="rounded-[1.5rem] border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:rounded-[2rem] sm:p-8">
      <div class="max-w-3xl">
        <p class="text-xs font-medium uppercase tracking-[0.18em] text-zinc-500 sm:text-sm">
          Documentation
        </p>

        <h1 class="mt-3 text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-4xl">
          Guides et tutoriels
        </h1>

        <p class="mt-4 text-sm leading-6 text-zinc-600 dark:text-zinc-300 sm:text-base sm:leading-7">
          Un espace documentaire plus structuré avec recherche, navigation et rendu enrichi.
        </p>
      </div>

      <div class="mt-6 space-y-8 sm:mt-8">
        {#each data.docsNavGroups as group}
          <section>
            <h2 class="text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-2xl">
              {group.name}
            </h2>

            <div class="mt-4 space-y-6 sm:mt-5">
              {#each group.categories as category}
                <div>
                  <h3 class="text-xs font-semibold uppercase tracking-[0.14em] text-zinc-500 sm:text-sm">
                    {category.name}
                  </h3>

                  <div class="mt-3 grid gap-3 sm:gap-4 md:grid-cols-2 xl:grid-cols-3">
                    {#each category.items as item}
                      {@const tutorial = data.tutorials.find((t) => t.slug === item.slug)}
                      {#if tutorial}
                        <a
                          href={`/tutos/${tutorial.slug}`}
                          class="group rounded-3xl border border-zinc-200 bg-zinc-50 p-4 transition hover:-translate-y-0.5 hover:border-zinc-300 hover:bg-white hover:shadow-md dark:border-zinc-800 dark:bg-zinc-950/50 dark:hover:border-zinc-700 dark:hover:bg-zinc-900 sm:p-5"
                        >
                          <div class="flex flex-wrap items-center gap-2">
                            <TutorialBadge text={tutorial.level} variant="level" />
                            <TutorialBadge text={tutorial.category} variant="category" />
                          </div>

                          <h4 class="mt-4 text-lg font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-xl">
                            {tutorial.title}
                          </h4>

                          <p class="mt-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
                            {tutorial.description}
                          </p>

                          <div class="mt-5 flex items-center justify-between gap-3 text-xs text-zinc-500 dark:text-zinc-400">
                            <span>{tutorial.duration}</span>
                            <span class="shrink-0">{tutorial.steps.length} étapes</span>
                          </div>
                        </a>
                      {/if}
                    {/each}
                  </div>
                </div>
              {/each}
            </div>
          </section>
        {/each}
      </div>
    </div>
  </div>
</section>