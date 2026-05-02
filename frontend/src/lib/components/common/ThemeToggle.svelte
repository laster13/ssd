<script lang="ts">
	import { onMount } from 'svelte';

	let theme = $state<'light' | 'dark'>('dark');
	let mounted = $state(false);

	function applyTheme(nextTheme: 'light' | 'dark') {
		theme = nextTheme;

		if (nextTheme === 'dark') {
			document.documentElement.classList.add('dark');
		} else {
			document.documentElement.classList.remove('dark');
		}

		localStorage.setItem('theme', nextTheme);
	}

	function toggleTheme() {
		applyTheme(theme === 'dark' ? 'light' : 'dark');
	}

	onMount(() => {
		const stored = localStorage.getItem('theme');
		const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		const initial =
			stored === 'light' || stored === 'dark' ? stored : systemDark ? 'dark' : 'light';

		applyTheme(initial);
		mounted = true;
	});
</script>

{#if mounted}
	<button
		type="button"
		onclick={toggleTheme}
		aria-label={theme === 'dark' ? 'Passer en mode clair' : 'Passer en mode sombre'}
		class="inline-flex h-11 w-11 items-center justify-center rounded-[16px] border border-black/8 bg-white/85 text-zinc-800 shadow-[0_10px_24px_rgba(15,23,42,0.06),inset_0_1px_0_rgba(255,255,255,0.92)] transition-all duration-300 hover:-translate-y-0.5 hover:rotate-6 hover:border-black/12 hover:bg-white hover:shadow-[0_14px_30px_rgba(15,23,42,0.10)] dark:border-white/10 dark:bg-white/[0.06] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18),inset_0_1px_0_rgba(255,255,255,0.05)] dark:hover:border-white/20 dark:hover:bg-white/[0.10] dark:hover:shadow-[0_14px_30px_rgba(0,0,0,0.24)]"
	>
		{#if theme === 'dark'}
			<svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" aria-hidden="true">
				<circle cx="12" cy="12" r="4.25" stroke="currentColor" stroke-width="1.8" />
				<path d="M12 2.75V5.25" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M12 18.75V21.25" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M21.25 12H18.75" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M5.25 12H2.75" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M18.54 5.46L16.77 7.23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M7.23 16.77L5.46 18.54" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M18.54 18.54L16.77 16.77" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				<path d="M7.23 7.23L5.46 5.46" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
			</svg>
		{:else}
			<svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" aria-hidden="true">
				<path
					d="M20.2 15.1A8.5 8.5 0 0 1 8.9 3.8a8.5 8.5 0 1 0 11.3 11.3Z"
					stroke="currentColor"
					stroke-width="1.8"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
		{/if}
	</button>
{/if}