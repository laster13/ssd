<script lang="ts">
  import type { TutorialIcon } from '$lib/data/tutorials';
  import { getTutorialTheme, type TutorialTheme } from '$lib/utils/tutorial-theme';
  import TutorialIconComponent from './TutorialIcon.svelte';

  let {
    title,
    items = [],
    tone = 'default',
    icon,
    theme = getTutorialTheme()
  }: {
    title: string;
    items?: string[];
    tone?: 'default' | 'warning';
    icon?: TutorialIcon;
    theme?: TutorialTheme;
  } = $props();

  const toneClass =
    tone === 'warning'
      ? 'border-amber-200 bg-amber-50 dark:border-amber-900/40 dark:bg-amber-950/20'
      : theme.panel;

  const textClass =
    tone === 'warning'
      ? 'text-amber-800 dark:text-amber-300'
      : 'text-zinc-600 dark:text-zinc-300';

  const titleClass =
    tone === 'warning'
      ? 'text-amber-900 dark:text-amber-200'
      : theme.sectionTitle;

  const iconClass =
    tone === 'warning'
      ? 'bg-white/70 text-amber-800 dark:bg-black/20 dark:text-amber-200'
      : `${theme.panelSoft} ${theme.sectionTitle}`;
</script>

<section class={`rounded-3xl border p-6 shadow-sm ${toneClass}`}>
  <div class="flex items-center gap-3">
    {#if icon}
      <div class={`flex h-10 w-10 items-center justify-center rounded-2xl ${iconClass}`}>
        <TutorialIconComponent name={icon} className="h-5 w-5" />
      </div>
    {/if}

    <h2 class={`text-xl font-semibold tracking-tight ${titleClass}`}>
      {title}
    </h2>
  </div>

  <ul class={`mt-4 space-y-3 text-sm ${textClass}`}>
    {#each items as item}
      <li class="flex gap-3">
        <span class={`mt-[2px] shrink-0 ${tone === 'warning' ? 'text-amber-600 dark:text-amber-400' : theme.sectionTitle}`}>•</span>
        <span>{item}</span>
      </li>
    {/each}
  </ul>
</section>