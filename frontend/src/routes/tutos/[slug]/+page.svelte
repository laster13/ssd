<script lang="ts">
  import { tick } from 'svelte';
  import DocsSidebar from '$lib/components/tutorials/DocsSidebar.svelte';
  import TableOfContents from '$lib/components/tutorials/TableOfContents.svelte';
  import MobileArticleActions from '$lib/components/tutorials/MobileArticleActions.svelte';
  import TutorialBadge from '$lib/components/tutorials/TutorialBadge.svelte';
  import TutorialSectionCard from '$lib/components/tutorials/TutorialSectionCard.svelte';
  import TutorialStepCard from '$lib/components/tutorials/TutorialStepCard.svelte';
  import TutorialIcon from '$lib/components/tutorials/TutorialIcon.svelte';
  import TutorialCallout from '$lib/components/tutorials/TutorialCallout.svelte';
  import TutorialImageCard from '$lib/components/tutorials/TutorialImageCard.svelte';
  import TutorialCodeBlock from '$lib/components/tutorials/TutorialCodeBlock.svelte';
  import TutorialDiagramCard from '$lib/components/tutorials/TutorialDiagramCard.svelte';
  import TutorialTabs from '$lib/components/tutorials/TutorialTabs.svelte';
  import TutorialAccordion from '$lib/components/tutorials/TutorialAccordion.svelte';
  import TutorialDiscussion from '$lib/components/forum/TutorialDiscussion.svelte';
  import { getTutorialTheme } from '$lib/utils/tutorial-theme';
  import type { DocsNavGroup, TocItem, Tutorial } from '$lib/data/tutorials';
  import type { ForumTopicListItem } from '$lib/types/forum';

  let {
    data,
    form
  }: {
    data: {
      tutorial: Tutorial;
      docsNavGroups: DocsNavGroup[];
      toc: TocItem[];
      forumTopics: ForumTopicListItem[];
      user: { email: string } | null;
      csrfToken: string;
    };
    form?: {
      createTopicError?: string;
      createTopicSuccess?: boolean;
      title?: string;
      content?: string;
    } | null;
  } = $props();

  const tutorial = $derived(data.tutorial);
  const docsNavGroups = $derived(data.docsNavGroups);
  const toc = $derived(data.toc);
  const forumTopics = $derived(data.forumTopics ?? []);
  const user = $derived(data.user ?? null);
  const csrfToken = $derived(data.csrfToken);
  const theme = $derived(getTutorialTheme(tutorial.category));

  let showMobileDocs = $state(false);
  let showMobileToc = $state(false);
  let openStepIndex = $state(0);

  function sectionId(section: NonNullable<Tutorial['sections']>[number]) {
    return (
      section.id ??
      section.title
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '')
    );
  }

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

  async function goToSteps() {
    await tick();
    document.getElementById('etapes')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
</script>

<svelte:head>
  <title>{tutorial.title} | SSD</title>
  <meta name="description" content={tutorial.description} />
</svelte:head>

{#key tutorial.slug}
<section class="mx-auto max-w-[1500px] overflow-x-hidden py-6 pb-28 sm:px-6 sm:py-10 sm:pb-10 lg:px-8">
  <div class="grid gap-6 xl:grid-cols-[280px_minmax(0,1fr)_280px] xl:gap-8">
    <div class="hidden space-y-4 sm:space-y-6 xl:block">
      <DocsSidebar groups={docsNavGroups} currentSlug={tutorial.slug} />
    </div>

    <div class="min-w-0">
      <div class="px-3 sm:px-0">
        <a
          href="/tutos"
          class="inline-flex items-center text-sm text-zinc-500 transition hover:text-zinc-900 dark:hover:text-zinc-100"
        >
          ← Retour à la documentation
        </a>

        <header class={`mt-4 overflow-hidden border-y sm:rounded-[2rem] sm:border sm:shadow-sm ${theme.panel}`}>
          <div class={`p-4 sm:p-8 ${theme.panelSoft}`}>
            <div class="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
              <div class="min-w-0 max-w-4xl">
                <div class="flex min-w-0 flex-wrap items-center gap-2">
                  {#if tutorial.icon}
                    <div class={`mr-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border sm:h-11 sm:w-11 ${theme.badge}`}>
                      <TutorialIcon name={tutorial.icon} className="h-5 w-5" />
                    </div>
                  {/if}

                  <TutorialBadge text={tutorial.level} variant="level" />
                  <TutorialBadge text={tutorial.category} variant="category" />
                  <TutorialBadge text={tutorial.duration} />
                </div>

                <h1 class={`mt-4 break-words text-2xl font-semibold tracking-tight sm:mt-5 sm:text-4xl ${theme.title}`}>
                  {tutorial.title}
                </h1>

                <p class="mt-3 max-w-3xl break-words text-sm leading-6 text-zinc-600 dark:text-zinc-300 sm:mt-4 sm:text-base sm:leading-7">
                  {tutorial.description}
                </p>

                {#if tutorial.summary}
                  <div class={`mt-4 rounded-2xl border p-4 text-sm leading-6 sm:mt-5 ${theme.callout}`}>
                    {tutorial.summary}
                  </div>
                {/if}

                {#if tutorial.tags?.length}
                  <div class="mt-4 flex flex-wrap gap-2 sm:mt-5">
                    {#each tutorial.tags as tag}
                      <span class={`inline-flex max-w-full items-center rounded-full border px-3 py-1 text-xs ${theme.badge}`}>
                        <span class="truncate">#{tag}</span>
                      </span>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
          </div>
        </header>
      </div>

      {#if tutorial.callouts?.length}
        <section id="introduction" class="mt-6 space-y-4 scroll-mt-24 sm:mt-8">
          {#each tutorial.callouts as callout}
            <TutorialCallout {callout} {theme} />
          {/each}
        </section>
      {/if}

      {#if tutorial.images?.length}
        <section id="captures" class="mt-6 space-y-4 scroll-mt-24 sm:mt-8">
          <div class="px-3 sm:px-0">
            <h2 class={`text-xl font-semibold tracking-tight sm:text-2xl ${theme.sectionTitle}`}>
              Captures
            </h2>
          </div>

          {#each tutorial.images as image}
            <TutorialImageCard {image} />
          {/each}
        </section>
      {/if}

      {#if tutorial.diagrams?.length}
        <section id="diagrammes" class="mt-6 space-y-4 scroll-mt-24 sm:mt-8">
          <div class="px-3 sm:px-0">
            <h2 class={`text-xl font-semibold tracking-tight sm:text-2xl ${theme.sectionTitle}`}>
              Diagrammes
            </h2>
          </div>

          {#each tutorial.diagrams as diagram}
            <TutorialDiagramCard {diagram} />
          {/each}
        </section>
      {/if}

      {#if tutorial.codeBlocks?.length}
        <section id="blocs-configuration" class="mt-6 space-y-4 scroll-mt-24 sm:mt-8">
          <div class="px-3 sm:px-0">
            <h2 class={`text-xl font-semibold tracking-tight sm:text-2xl ${theme.sectionTitle}`}>
              Blocs de configuration
            </h2>
          </div>

          {#each tutorial.codeBlocks as block}
            <TutorialCodeBlock {block} {theme} />
          {/each}
        </section>
      {/if}

      <section id="etapes" class="mt-6 space-y-5 scroll-mt-24 sm:mt-8 sm:space-y-6">
        <div class="px-3 sm:px-0">
          <div class="flex items-center justify-between gap-3">
            <div>
              <h2 class={`text-xl font-semibold tracking-tight sm:text-2xl ${theme.sectionTitle}`}>
                Étapes
              </h2>
              <p class="mt-1 text-sm text-zinc-500">{tutorial.steps.length} étapes</p>
            </div>

            <div class={`hidden rounded-full border px-3 py-1.5 text-xs font-medium sm:inline-flex ${theme.badge}`}>
              Timeline
            </div>
          </div>
        </div>

        <div class="space-y-1">
          {#each tutorial.steps as step, index}
            <TutorialStepCard
              {step}
              {index}
              {theme}
              open={openStepIndex === index}
              onToggle={() => (openStepIndex = openStepIndex === index ? -1 : index)}
            />
          {/each}
        </div>
      </section>

      {#if tutorial.sections?.length}
        {#each tutorial.sections as section}
          <section
            id={sectionId(section)}
            class="mt-6 space-y-4 scroll-mt-24 sm:mt-8"
          >
            <div class="px-3 sm:px-0">
              <h2 class={`text-xl font-semibold tracking-tight sm:text-2xl ${theme.sectionTitle}`}>
                {section.title}
              </h2>
            </div>

            {#if section.items?.length}
              <TutorialSectionCard title={section.title} items={section.items} icon={section.icon} {theme} />
            {/if}

            {#if section.body?.length}
              <section class={`border-y p-4 sm:rounded-3xl sm:border sm:p-6 sm:shadow-sm ${theme.panel}`}>
                <div class="space-y-3 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
                  {#each section.body as paragraph}
                    <p>{@html linkify(paragraph)}</p>
                  {/each}
                </div>
              </section>
            {/if}

            {#if section.callouts?.length}
              {#each section.callouts as callout}
                <TutorialCallout {callout} {theme} />
              {/each}
            {/if}

            {#if section.images?.length}
              {#each section.images as image}
                <TutorialImageCard {image} />
              {/each}
            {/if}

            {#if section.diagrams?.length}
              {#each section.diagrams as diagram}
                <TutorialDiagramCard {diagram} />
              {/each}
            {/if}

            {#if section.codeBlocks?.length}
              {#each section.codeBlocks as block}
                <TutorialCodeBlock {block} {theme} />
              {/each}
            {/if}

            {#if section.tabs?.length}
              <TutorialTabs tabs={section.tabs} />
            {/if}

            {#if section.accordions?.length}
              <div class="space-y-4">
                {#each section.accordions as item}
                  <TutorialAccordion {item} />
                {/each}
              </div>
            {/if}
          </section>
        {/each}
      {/if}

      <div class="mt-6 grid gap-4 sm:mt-8 sm:gap-6 lg:grid-cols-2">
        {#if tutorial.prerequisites?.length}
          <TutorialSectionCard title="Prérequis" items={tutorial.prerequisites} icon="rocket" {theme} />
        {/if}

        {#if tutorial.warnings?.length}
          <TutorialSectionCard title="Points d’attention" items={tutorial.warnings} tone="warning" icon="shield" {theme} />
        {/if}

        {#if tutorial.troubleshooting?.length}
          <TutorialSectionCard title="En cas de problème" items={tutorial.troubleshooting} tone="warning" icon="bug" {theme} />
        {/if}

        {#if tutorial.finalChecklist?.length}
          <section class={`border-y p-4 sm:rounded-3xl sm:border sm:p-6 sm:shadow-sm ${theme.panel}`}>
            <div class="px-3 sm:px-0">
              <h2 class={`text-xl font-semibold tracking-tight ${theme.sectionTitle}`}>
                Checklist finale
              </h2>
            </div>

            <ul class="mt-4 space-y-3 text-sm text-zinc-600 dark:text-zinc-300">
              {#each tutorial.finalChecklist as item}
                <li class="flex gap-3">
                  <span class="mt-[2px] shrink-0 text-emerald-600">✓</span>
                  <span>{item}</span>
                </li>
              {/each}
            </ul>
          </section>
        {/if}
      </div>

      <TutorialDiscussion
        tutorial={{ slug: tutorial.slug, title: tutorial.title }}
        topics={forumTopics}
        {user}
        {csrfToken}
        {form}
      />
    </div>

    <div class="hidden xl:block">
      <TableOfContents items={toc} />
    </div>
  </div>

  <MobileArticleActions
    onDocs={() => (showMobileDocs = true)}
    onToc={() => (showMobileToc = true)}
    onSteps={goToSteps}
  />

  {#if showMobileDocs}
    <div class="xl:hidden">
      <div class="fixed inset-0 z-[90] bg-black/40 backdrop-blur-sm" onclick={() => (showMobileDocs = false)}>
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
                onclick={() => (showMobileDocs = false)}
                class="rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
              >
                Fermer
              </button>
            </div>

            <div class="max-h-[78vh] overflow-y-auto p-4">
              <div class="mb-4 flex flex-col gap-2">
                <a
                  href="/"
                  onclick={() => (showMobileDocs = false)}
                  class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm font-medium text-zinc-800 transition hover:bg-white dark:border-zinc-800 dark:bg-zinc-950/40 dark:text-zinc-100"
                >
                  ← Retour à l’accueil
                </a>

                <a
                  href="/tutos"
                  onclick={() => (showMobileDocs = false)}
                  class="rounded-2xl border border-zinc-200 bg-zinc-50 px-4 py-3 text-sm font-medium text-zinc-800 transition hover:bg-white dark:border-zinc-800 dark:bg-zinc-950/40 dark:text-zinc-100"
                >
                  Voir toute la documentation
                </a>
              </div>

              <div class="space-y-5">
                {#each docsNavGroups as group}
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
                                  onclick={() => (showMobileDocs = false)}
                                  aria-current={tutorial.slug === item.slug ? 'page' : undefined}
                                  class={`block rounded-xl px-3 py-2 text-sm leading-5 transition ${
                                    tutorial.slug === item.slug
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
    </div>
  {/if}

  {#if showMobileToc}
    <div class="xl:hidden">
      <div class="fixed inset-0 z-[90] bg-black/40 backdrop-blur-sm" onclick={() => (showMobileToc = false)}>
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
                onclick={() => (showMobileToc = false)}
                class="rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
              >
                Fermer
              </button>
            </div>

            <div class="max-h-[70vh] overflow-y-auto p-4">
              <ul class="space-y-2">
                {#each toc as item}
                  <li>
                    <a
                      href={`#${item.id}`}
                      onclick={() => (showMobileToc = false)}
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
    </div>
  {/if}
</section>
{/key}