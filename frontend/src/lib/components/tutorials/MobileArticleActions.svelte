<script lang="ts">
  let {
    onDocs,
    onToc,
    onSteps
  }: {
    onDocs: () => void;
    onToc: () => void;
    onSteps: () => void;
  } = $props();
</script>

<div class="xl:hidden">
  <div class="fixed inset-x-0 bottom-3 z-[70] px-3">
    <div class="mx-auto max-w-xl rounded-2xl border border-zinc-200/80 bg-white/95 p-2 shadow-[0_18px_50px_rgba(15,23,42,0.18)] backdrop-blur dark:border-zinc-800 dark:bg-zinc-900/95 dark:shadow-[0_18px_50px_rgba(0,0,0,0.35)]">
      <div class="grid grid-cols-3 gap-2">
        <button
          type="button"
          onclick={onDocs}
          class="rounded-xl px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:text-zinc-200 dark:hover:bg-zinc-800"
        >
          Docs
        </button>

        <button
          type="button"
          onclick={onToc}
          class="rounded-xl px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:text-zinc-200 dark:hover:bg-zinc-800"
        >
          Sommaire
        </button>

        <button
          type="button"
          onclick={onSteps}
          class="rounded-xl px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:text-zinc-200 dark:hover:bg-zinc-800"
        >
          Étapes
        </button>
      </div>
    </div>
  </div>
</div>