<script lang="ts">
  let {
    open = false,
    title = '',
    onClose,
    mode = 'default'
  }: {
    open: boolean;
    title?: string;
    onClose: () => void;
    mode?: 'default' | 'image';
  } = $props();

  function handleBackdropClick() {
    onClose();
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      onClose();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if open}
  <div
    class="fixed inset-0 z-[100] bg-black/80 backdrop-blur-sm"
    on:click={handleBackdropClick}
  >
    <div class="flex min-h-full items-end justify-center p-2 sm:items-center sm:p-6 lg:p-10">
      <div
        class={`relative w-full rounded-t-3xl border border-white/10 bg-zinc-950 shadow-2xl sm:rounded-3xl ${
          mode === 'image' ? 'max-w-[98vw] sm:max-w-[95vw]' : 'max-w-6xl'
        }`}
        on:click|stopPropagation
      >
        <div class="flex items-center justify-between gap-4 border-b border-white/10 px-4 py-4 sm:px-5">
          <h2 class="text-sm font-semibold tracking-tight text-white sm:text-base">
            {title}
          </h2>

          <button
            type="button"
            on:click={onClose}
            class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-white transition hover:bg-white/10"
          >
            Fermer
          </button>
        </div>

        <div class="max-h-[88vh] overflow-auto p-3 sm:max-h-[85vh] sm:p-6">
          <slot />
        </div>
      </div>
    </div>
  </div>
{/if}