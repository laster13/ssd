<script lang="ts">
  type Variant = 'level' | 'category' | 'neutral';

  let {
    text,
    variant = 'neutral'
  }: {
    text: string;
    variant?: Variant;
  } = $props();

  const styles = {
    level: 'bg-zinc-900 text-white dark:bg-white dark:text-zinc-900',
    category: 'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200',
    neutral: 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-300'
  };
</script>

<span class={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${styles[variant]}`}>
  {text}
</span>