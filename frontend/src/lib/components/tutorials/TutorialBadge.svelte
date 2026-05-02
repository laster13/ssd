<script lang="ts">
	type Variant = 'level' | 'category' | 'neutral';

	let {
		text,
		variant = 'neutral'
	}: {
		text: string;
		variant?: Variant;
	} = $props();

	function normalize(value: string) {
		return value
			.normalize('NFD')
			.replace(/[\u0300-\u036f]/g, '')
			.trim()
			.toLowerCase();
	}

	const neutralClass =
		'border border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200';

	function levelClass(value: string) {
		const key = normalize(value);

		if (key.includes('debut')) {
			return 'border border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
		}

		if (key.includes('inter')) {
			return 'border border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300';
		}

		if (key.includes('avance') || key.includes('expert')) {
			return 'border border-violet-200 bg-violet-50 text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300';
		}

		return 'border border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
	}

	function categoryClass(value: string) {
		const key = normalize(value);

		if (key.includes('config')) {
			return 'border border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300';
		}

		if (key.includes('install')) {
			return 'border border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-500/20 dark:bg-emerald-500/10 dark:text-emerald-300';
		}

		if (key.includes('secur')) {
			return 'border border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-500/20 dark:bg-rose-500/10 dark:text-rose-300';
		}

		if (key.includes('reseau')) {
			return 'border border-violet-200 bg-violet-50 text-violet-700 dark:border-violet-500/20 dark:bg-violet-500/10 dark:text-violet-300';
		}

		if (key.includes('docker')) {
			return 'border border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-500/20 dark:bg-cyan-500/10 dark:text-cyan-300';
		}

		if (key.includes('maint')) {
			return 'border border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-500/20 dark:bg-amber-500/10 dark:text-amber-300';
		}

		if (key.includes('depan') || key.includes('debug') || key.includes('troubles')) {
			return 'border border-orange-200 bg-orange-50 text-orange-700 dark:border-orange-500/20 dark:bg-orange-500/10 dark:text-orange-300';
		}

		if (key.includes('monitor')) {
			return 'border border-teal-200 bg-teal-50 text-teal-700 dark:border-teal-500/20 dark:bg-teal-500/10 dark:text-teal-300';
		}

		if (key.includes('stock')) {
			return 'border border-fuchsia-200 bg-fuchsia-50 text-fuchsia-700 dark:border-fuchsia-500/20 dark:bg-fuchsia-500/10 dark:text-fuchsia-300';
		}

		return 'border border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-500/20 dark:bg-indigo-500/10 dark:text-indigo-300';
	}

	function getClass(value: string, currentVariant: Variant) {
		if (currentVariant === 'level') return levelClass(value);
		if (currentVariant === 'category') return categoryClass(value);
		return neutralClass;
	}
</script>

<span
	class={`inline-flex max-w-full items-center rounded-full px-3 py-1 text-xs font-semibold ${getClass(text, variant)}`}
>
	<span class="truncate">{text}</span>
</span>