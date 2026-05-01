<script lang="ts">
  import type { TutorialImage } from '$lib/data/tutorials';
  import TutorialLightbox from './TutorialLightbox.svelte';

  let {
    image
  }: {
    image: TutorialImage;
  } = $props();

  let open = $state(false);
</script>

<figure class="overflow-hidden rounded-3xl border border-zinc-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
  <button
    type="button"
    on:click={() => (open = true)}
    class="block w-full text-left"
  >
    <div class="flex items-center justify-center bg-zinc-50 p-2 sm:p-3 dark:bg-zinc-950/50">
      <img
        src={image.src}
        alt={image.alt}
        class="max-h-[220px] w-auto max-w-full rounded-2xl object-contain transition hover:scale-[1.01] sm:max-h-[320px]"
        loading="lazy"
      />
    </div>
  </button>

  <figcaption class="border-t border-zinc-200 px-4 py-3 dark:border-zinc-800">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
      <div class="text-sm leading-6 text-zinc-600 dark:text-zinc-300">
        {#if image.caption}
          {image.caption}
        {:else}
          {image.alt}
        {/if}
      </div>

      <button
        type="button"
        on:click={() => (open = true)}
        class="self-start rounded-xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-xs font-medium text-zinc-700 transition hover:bg-white dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200"
      >
        Agrandir
      </button>
    </div>
  </figcaption>
</figure>

<TutorialLightbox
  open={open}
  title={image.caption || image.alt}
  onClose={() => (open = false)}
  mode="image"
>
  <div class="space-y-4">
    <div class="flex justify-end">
      <a
        href={image.src}
        target="_blank"
        rel="noreferrer"
        class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white transition hover:bg-white/10"
      >
        Ouvrir en taille réelle
      </a>
    </div>

    <div class="flex items-center justify-center overflow-auto">
      <img
        src={image.src}
        alt={image.alt}
        class="h-auto max-w-none rounded-2xl"
      />
    </div>
  </div>
</TutorialLightbox>