<script lang="ts">
  import { onMount } from 'svelte';
  import type { TutorialDiagram } from '$lib/data/tutorials';
  import TutorialLightbox from './TutorialLightbox.svelte';

  let {
    diagram
  }: {
    diagram: TutorialDiagram;
  } = $props();

  let previewContainer: HTMLDivElement | null = null;
  let modalContainer: HTMLDivElement | null = null;
  let errorMessage = $state('');
  let open = $state(false);
  let renderedSvg = '';

  async function renderMermaid() {
    try {
      const mermaid = (await import('mermaid')).default;

      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose'
      });

      const id = `mermaid-${crypto.randomUUID()}`;
      const { svg } = await mermaid.render(id, diagram.code);
      renderedSvg = svg;

      if (previewContainer) {
        previewContainer.innerHTML = svg;
      }

      if (modalContainer) {
        modalContainer.innerHTML = svg;
      }
    } catch (error) {
      errorMessage = 'Impossible de rendre le diagramme Mermaid.';
      console.error(error);
    }
  }

  onMount(async () => {
    await renderMermaid();
  });

  $effect(() => {
    if (open && modalContainer && renderedSvg) {
      modalContainer.innerHTML = renderedSvg;
    }
  });
</script>

<section class="rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
  {#if diagram.title}
    <div class="flex flex-col gap-3 border-b border-zinc-200 px-4 py-4 dark:border-zinc-800 sm:flex-row sm:items-center sm:justify-between sm:px-5">
      <div>
        <h3 class="text-base font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
          {diagram.title}
        </h3>
        <p class="mt-1 text-xs uppercase tracking-[0.14em] text-zinc-500">Mermaid</p>
      </div>

      <button
        type="button"
        on:click={() => (open = true)}
        class="self-start rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-700 transition hover:bg-white dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
      >
        Agrandir
      </button>
    </div>
  {/if}

  <div class="p-3 sm:p-4">
    {#if errorMessage}
      <div class="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900/40 dark:bg-red-950/20 dark:text-red-300">
        {errorMessage}
      </div>

      <pre class="mt-4 overflow-x-auto rounded-2xl bg-zinc-950 p-4 text-sm text-zinc-100">{diagram.code}</pre>
    {:else}
      <button
        type="button"
        on:click={() => (open = true)}
        class="block w-full overflow-hidden rounded-2xl border border-zinc-200 bg-zinc-50 p-3 text-left dark:border-zinc-800 dark:bg-zinc-950/40 sm:p-4"
      >
        <div class="overflow-auto">
          <div
            bind:this={previewContainer}
            class="origin-top-left scale-[0.82] sm:scale-[0.88] lg:scale-[0.95]"
            style="width: max-content;"
          ></div>
        </div>
      </button>
    {/if}
  </div>
</section>

<TutorialLightbox
  open={open}
  title={diagram.title || 'Diagramme Mermaid'}
  onClose={() => (open = false)}
>
  {#if errorMessage}
    <pre class="overflow-x-auto rounded-2xl bg-zinc-950 p-4 text-sm text-zinc-100">{diagram.code}</pre>
  {:else}
    <div class="overflow-auto">
      <div
        bind:this={modalContainer}
        class="min-w-max rounded-2xl bg-white p-3 sm:p-4"
      ></div>
    </div>
  {/if}
</TutorialLightbox>