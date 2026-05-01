<script lang="ts">
  import type { TutorialStep } from '$lib/data/tutorials';
  import TutorialIcon from './TutorialIcon.svelte';

  let {
    step,
    index,
    open = false,
    onToggle = () => {}
  }: {
    step: TutorialStep;
    index: number;
    open?: boolean;
    onToggle?: () => void;
  } = $props();
</script>

<article class="relative">
  <div class="absolute left-[21px] top-14 bottom-0 w-px bg-zinc-200 dark:bg-zinc-800 sm:left-[23px]"></div>

  <div class="relative flex items-start gap-3 sm:gap-4">
    <button
      type="button"
      onclick={onToggle}
      class={`relative z-10 flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border text-sm font-semibold transition sm:h-12 sm:w-12 ${
        open
          ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
          : 'border-zinc-200 bg-white text-zinc-700 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-200'
      }`}
      aria-expanded={open}
      aria-label={`Étape ${index + 1}`}
    >
      {index + 1}
    </button>

    <div class="min-w-0 flex-1 pb-5">
      <button
        type="button"
        onclick={onToggle}
        class="block w-full rounded-[24px] border border-zinc-200 bg-white p-4 text-left shadow-sm transition hover:border-zinc-300 dark:border-zinc-800 dark:bg-zinc-900 dark:hover:border-zinc-700 sm:p-5"
      >
        <div class="flex items-start gap-3">
          <div class="mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200">
            {#if step.icon}
              <TutorialIcon name={step.icon} className="h-5 w-5" />
            {:else}
              <span>•</span>
            {/if}
          </div>

          <div class="min-w-0 flex-1">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="text-lg font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 sm:text-xl">
                  {step.title}
                </h3>

                <p class="mt-2 text-sm leading-6 text-zinc-500 dark:text-zinc-400">
                  Étape {index + 1}
                </p>
              </div>

              <div class="shrink-0 rounded-xl bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-500 dark:bg-zinc-800 dark:text-zinc-300">
                {open ? '−' : '+'}
              </div>
            </div>
          </div>
        </div>
      </button>

      {#if open}
        <div class="ml-2 mt-3 rounded-[24px] border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900 sm:p-5">
          <p class="text-sm leading-7 text-zinc-700 dark:text-zinc-300 sm:text-base">
            {step.text}
          </p>

          {#if step.code}
            <div class="mt-4 overflow-x-auto rounded-2xl bg-zinc-950 p-4 text-sm text-zinc-100">
              <pre class="min-w-max whitespace-pre font-mono">{step.code}</pre>
            </div>
          {/if}

          {#if step.result}
            <div class="mt-4 rounded-2xl border border-emerald-200/80 bg-emerald-50/80 p-4 dark:border-emerald-900/40 dark:bg-emerald-950/20">
              <div class="flex items-start gap-3">
                <div class="mt-0.5 shrink-0 text-emerald-600 dark:text-emerald-400">✓</div>

                <div>
                  <div class="text-sm font-semibold text-emerald-800 dark:text-emerald-300">
                    Résultat attendu
                  </div>
                  <p class="mt-1 text-sm leading-6 text-emerald-800/90 dark:text-emerald-300">
                    {step.result}
                  </p>
                </div>
              </div>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
</article>