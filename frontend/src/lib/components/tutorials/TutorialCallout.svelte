<script lang="ts">
  import type { TutorialCallout, TutorialCalloutTone } from '$lib/data/tutorials';

  let {
    callout
  }: {
    callout: TutorialCallout;
  } = $props();

  const styles: Record<TutorialCalloutTone, { box: string; title: string; text: string }> = {
    abstract: {
      box: 'border-sky-200 bg-sky-50 dark:border-sky-900/40 dark:bg-sky-950/20',
      title: 'text-sky-900 dark:text-sky-200',
      text: 'text-sky-800 dark:text-sky-300'
    },
    tip: {
      box: 'border-emerald-200 bg-emerald-50 dark:border-emerald-900/40 dark:bg-emerald-950/20',
      title: 'text-emerald-900 dark:text-emerald-200',
      text: 'text-emerald-800 dark:text-emerald-300'
    },
    info: {
      box: 'border-blue-200 bg-blue-50 dark:border-blue-900/40 dark:bg-blue-950/20',
      title: 'text-blue-900 dark:text-blue-200',
      text: 'text-blue-800 dark:text-blue-300'
    },
    warning: {
      box: 'border-amber-200 bg-amber-50 dark:border-amber-900/40 dark:bg-amber-950/20',
      title: 'text-amber-900 dark:text-amber-200',
      text: 'text-amber-800 dark:text-amber-300'
    },
    danger: {
      box: 'border-red-200 bg-red-50 dark:border-red-900/40 dark:bg-red-950/20',
      title: 'text-red-900 dark:text-red-200',
      text: 'text-red-800 dark:text-red-300'
    },
    success: {
      box: 'border-emerald-200 bg-emerald-50 dark:border-emerald-900/40 dark:bg-emerald-950/20',
      title: 'text-emerald-900 dark:text-emerald-200',
      text: 'text-emerald-800 dark:text-emerald-300'
    }
  };

  const tone = styles[callout.tone];

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
</script>

<section class={`rounded-3xl border p-5 shadow-sm ${tone.box}`}>
  <h3 class={`text-base font-semibold tracking-tight ${tone.title}`}>
    {callout.title}
  </h3>

  <div class={`mt-3 space-y-2 text-sm leading-6 ${tone.text}`}>
    {#each callout.content as paragraph}
      <p>{@html linkify(paragraph)}</p>
    {/each}
  </div>
</section>