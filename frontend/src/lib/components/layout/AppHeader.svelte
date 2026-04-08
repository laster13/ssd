<script lang="ts">
	import { onMount } from 'svelte';

	type User = {
		email?: string;
		is_admin?: boolean;
	};

	let {
		user,
		csrfToken,
		pathname = '/'
	}: {
		user?: User | null;
		csrfToken?: string;
		pathname?: string;
	} = $props();

	let theme = $state<'light' | 'dark'>('dark');
	let mounted = $state(false);
	let mobileMenuOpen = $state(false);
	let userMenuOpen = $state(false);

	const navItems = [
		{ label: 'App Store', href: '/app-store' },
		{ label: 'Serveurs', href: '/servers' },
		{ label: 'Applications', href: '/applications' },
		{ label: 'Stream-Fusion', href: '/settings/streamfusion' }
	];

	function isActive(href: string) {
		return pathname === href || pathname.startsWith(`${href}/`);
	}

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

	function closeMenus() {
		mobileMenuOpen = false;
		userMenuOpen = false;
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

<svelte:window onkeydown={(e) => e.key === 'Escape' && closeMenus()} />

<header class="sticky top-0 z-50 border-b border-black/5 bg-white/75 backdrop-blur-2xl supports-[backdrop-filter]:bg-white/70 dark:border-white/10 dark:bg-[rgba(6,7,11,0.76)]">
	<div class="pointer-events-none absolute inset-0 overflow-hidden">
		<div class="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.88),rgba(255,255,255,0.58))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.035),rgba(255,255,255,0.01))]"></div>
		<div class="absolute inset-x-0 top-0 h-px bg-white/70 dark:bg-white/10"></div>
	</div>

	<div class="relative mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-[18px] sm:px-6 lg:px-8">
		<div class="flex min-w-0 items-center gap-3 sm:gap-4">
			<button
				type="button"
				onclick={() => {
					mobileMenuOpen = !mobileMenuOpen;
					userMenuOpen = false;
				}}
				aria-label="Ouvrir le menu"
				class="inline-flex h-11 w-11 items-center justify-center rounded-[16px] border border-black/8 bg-white/85 text-zinc-800 shadow-[0_10px_24px_rgba(15,23,42,0.06),inset_0_1px_0_rgba(255,255,255,0.92)] transition-all duration-300 hover:-translate-y-0.5 hover:border-black/12 hover:bg-white hover:shadow-[0_14px_30px_rgba(15,23,42,0.10)] lg:hidden dark:border-white/10 dark:bg-white/[0.06] dark:text-white dark:shadow-[0_10px_24px_rgba(0,0,0,0.18),inset_0_1px_0_rgba(255,255,255,0.05)] dark:hover:border-white/20 dark:hover:bg-white/[0.10] dark:hover:shadow-[0_14px_30px_rgba(0,0,0,0.24)]"
			>
				<svg viewBox="0 0 24 24" class="h-5 w-5" fill="none" aria-hidden="true">
					<path d="M4 7H20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
					<path d="M4 12H20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
					<path d="M4 17H20" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
				</svg>
			</button>

			<a
				href="/"
				class="group inline-flex shrink-0 items-center gap-3 rounded-[20px] border border-black/6 bg-white/85 px-3.5 py-2.5 shadow-[0_14px_34px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.95)] transition-all duration-300 hover:-translate-y-0.5 hover:border-black/10 hover:bg-white hover:shadow-[0_18px_40px_rgba(15,23,42,0.12),inset_0_1px_0_rgba(255,255,255,1)] dark:border-white/10 dark:bg-white/[0.04] dark:shadow-[0_14px_34px_rgba(0,0,0,0.22),inset_0_1px_0_rgba(255,255,255,0.05)] dark:hover:border-white/20 dark:hover:bg-white/[0.07] dark:hover:shadow-[0_18px_40px_rgba(0,0,0,0.30),inset_0_1px_0_rgba(255,255,255,0.07)]"
			>
				<div class="relative flex h-12 w-12 items-center justify-center overflow-hidden rounded-[18px] border border-black/6 bg-[linear-gradient(135deg,rgba(34,211,238,0.28),rgba(168,85,247,0.28))] shadow-[0_14px_30px_rgba(15,23,42,0.12),inset_0_1px_0_rgba(255,255,255,0.65)] dark:border-white/10 dark:shadow-[0_14px_30px_rgba(0,0,0,0.28),inset_0_1px_0_rgba(255,255,255,0.06)]">
					<div class="absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.42),rgba(255,255,255,0.10))] dark:bg-[linear-gradient(to_bottom,rgba(255,255,255,0.20),rgba(255,255,255,0.03))]"></div>

					<svg viewBox="0 0 64 64" class="relative h-6 w-6" fill="none" aria-hidden="true">
						<defs>
							<linearGradient id="ssdLogoGradient" x1="8" y1="8" x2="56" y2="56" gradientUnits="userSpaceOnUse">
								<stop offset="0%" stop-color="#22d3ee" />
								<stop offset="55%" stop-color="#60a5fa" />
								<stop offset="100%" stop-color="#a855f7" />
							</linearGradient>
						</defs>
						<rect x="10" y="10" width="44" height="44" rx="14" fill="url(#ssdLogoGradient)" fill-opacity="0.18" />
						<path
							d="M22 24.5C22 21.4624 24.4624 19 27.5 19H37.5C40.5376 19 43 21.4624 43 24.5C43 27.5376 40.5376 30 37.5 30H26.5C24.567 30 23 31.567 23 33.5C23 35.433 24.567 37 26.5 37H37C39.2091 37 41 38.7909 41 41C41 43.2091 39.2091 45 37 45H22"
							stroke="url(#ssdLogoGradient)"
							stroke-width="4.2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</div>

				<div class="hidden sm:block">
					<div class="text-[13px] font-semibold tracking-[0.18em] text-zinc-950 dark:text-white">
						SSD
					</div>
				</div>
			</a>

			<nav class="hidden items-center gap-2 lg:flex">
				{#each navItems as item}
					<a
						href={item.href}
						aria-current={isActive(item.href) ? 'page' : undefined}
						class={`group relative inline-flex items-center rounded-full px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] transition-all duration-300 ${
							isActive(item.href)
								? 'border border-black/8 bg-white text-zinc-950 shadow-[0_10px_26px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.95)] dark:border-white/15 dark:bg-white/[0.12] dark:text-white dark:shadow-[0_8px_24px_rgba(0,0,0,0.18),inset_0_1px_0_rgba(255,255,255,0.06)]'
								: 'border border-transparent text-zinc-500 hover:-translate-y-[1px] hover:border-black/8 hover:bg-white/70 hover:text-zinc-950 hover:shadow-[0_8px_20px_rgba(15,23,42,0.05)] dark:text-zinc-400 dark:hover:border-white/10 dark:hover:bg-white/[0.05] dark:hover:text-white dark:hover:shadow-none'
						}`}
					>
						{#if isActive(item.href)}
							<span class="absolute inset-x-3 bottom-1 h-px bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.8),rgba(168,85,247,0.8),transparent)] dark:bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.7),rgba(168,85,247,0.7),transparent)]"></span>
						{/if}
						{item.label}
					</a>
				{/each}

				{#if user}
					<a
						href="/settings/security"
						aria-current={isActive('/settings/security') ? 'page' : undefined}
						class={`group relative inline-flex items-center rounded-full px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] transition-all duration-300 ${
							isActive('/settings/security')
								? 'border border-black/8 bg-white text-zinc-950 shadow-[0_10px_26px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.95)] dark:border-white/15 dark:bg-white/[0.12] dark:text-white dark:shadow-[0_8px_24px_rgba(0,0,0,0.18),inset_0_1px_0_rgba(255,255,255,0.06)]'
								: 'border border-transparent text-zinc-500 hover:-translate-y-[1px] hover:border-black/8 hover:bg-white/70 hover:text-zinc-950 hover:shadow-[0_8px_20px_rgba(15,23,42,0.05)] dark:text-zinc-400 dark:hover:border-white/10 dark:hover:bg-white/[0.05] dark:hover:text-white dark:hover:shadow-none'
						}`}
					>
						{#if isActive('/settings/security')}
							<span class="absolute inset-x-3 bottom-1 h-px bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.8),rgba(168,85,247,0.8),transparent)] dark:bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.7),rgba(168,85,247,0.7),transparent)]"></span>
						{/if}
						Sécurité
					</a>
				{/if}

				{#if user?.is_admin}
					<a
						href="/admin"
						aria-current={isActive('/admin') ? 'page' : undefined}
						class={`group relative inline-flex items-center rounded-full px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.12em] transition-all duration-300 ${
							isActive('/admin')
								? 'border border-black/8 bg-white text-zinc-950 shadow-[0_10px_26px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.95)] dark:border-white/15 dark:bg-white/[0.12] dark:text-white dark:shadow-[0_8px_24px_rgba(0,0,0,0.18),inset_0_1px_0_rgba(255,255,255,0.06)]'
								: 'border border-transparent text-zinc-500 hover:-translate-y-[1px] hover:border-black/8 hover:bg-white/70 hover:text-zinc-950 hover:shadow-[0_8px_20px_rgba(15,23,42,0.05)] dark:text-zinc-400 dark:hover:border-white/10 dark:hover:bg-white/[0.05] dark:hover:text-white dark:hover:shadow-none'
						}`}
					>
						{#if isActive('/admin')}
							<span class="absolute inset-x-3 bottom-1 h-px bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.8),rgba(168,85,247,0.8),transparent)] dark:bg-[linear-gradient(90deg,transparent,rgba(34,211,238,0.7),rgba(168,85,247,0.7),transparent)]"></span>
						{/if}
						Admin
					</a>
				{/if}
			</nav>
		</div>

		<div class="flex shrink-0 items-center gap-3">
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

			{#if user}
				<div class="relative hidden sm:block">
					<button
						type="button"
						onclick={() => {
							userMenuOpen = !userMenuOpen;
							mobileMenuOpen = false;
						}}
						class="inline-flex items-center gap-3 rounded-full border border-black/6 bg-white/80 px-3 py-2.5 shadow-[0_10px_26px_rgba(15,23,42,0.06),inset_0_1px_0_rgba(255,255,255,0.9)] transition-all duration-300 hover:-translate-y-0.5 hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_10px_26px_rgba(0,0,0,0.20),inset_0_1px_0_rgba(255,255,255,0.05)] dark:hover:border-white/20 dark:hover:bg-white/[0.07]"
					>
						<div class="flex h-10 w-10 items-center justify-center rounded-full border border-black/5 bg-[linear-gradient(135deg,rgba(34,211,238,0.12),rgba(168,85,247,0.16))] text-[12px] font-semibold text-zinc-950 shadow-[inset_0_1px_0_rgba(255,255,255,0.7)] dark:border-white/10 dark:text-white dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.05)]">
							{user.email?.slice(0, 1).toUpperCase() ?? 'U'}
						</div>

						<div class="max-w-[220px] text-left">
							<div class="truncate text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-500">
								Connecté
							</div>
							<div class="truncate text-sm font-medium text-zinc-800 dark:text-zinc-200">
								{user.email}
							</div>
						</div>

						<svg viewBox="0 0 24 24" class="h-4 w-4 text-zinc-500 dark:text-zinc-400" fill="none" aria-hidden="true">
							<path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
						</svg>
					</button>

					{#if userMenuOpen}
						<div class="absolute right-0 top-[calc(100%+12px)] z-50 w-64 overflow-hidden rounded-[22px] border border-black/8 bg-white/95 p-2 shadow-[0_20px_50px_rgba(15,23,42,0.14),inset_0_1px_0_rgba(255,255,255,0.95)] backdrop-blur-xl dark:border-white/10 dark:bg-[rgba(12,14,20,0.92)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.35),inset_0_1px_0_rgba(255,255,255,0.05)]">
							<div class="mb-2 rounded-[18px] border border-black/5 bg-black/[0.02] px-3 py-3 dark:border-white/5 dark:bg-white/[0.03]">
								<div class="truncate text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-500">
									Compte
								</div>
								<div class="mt-1 truncate text-sm font-medium text-zinc-900 dark:text-zinc-100">
									{user.email}
								</div>
							</div>

							<a
								href="/settings/security"
								onclick={() => (userMenuOpen = false)}
								class="flex items-center rounded-[16px] px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white"
							>
								Sécurité
							</a>

							{#if user?.is_admin}
								<a
									href="/admin"
									onclick={() => (userMenuOpen = false)}
									class="flex items-center rounded-[16px] px-3 py-3 text-sm font-medium text-zinc-700 transition hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white"
								>
									Admin
								</a>
							{/if}

							<div class="my-2 h-px bg-black/5 dark:bg-white/5"></div>

							<form method="POST" action="/logout" class="m-0">
								<input type="hidden" name="_csrf" value={csrfToken} />
								<button
									type="submit"
									class="flex w-full items-center rounded-[16px] px-3 py-3 text-left text-sm font-medium text-red-600 transition hover:bg-red-50 dark:text-red-300 dark:hover:bg-red-500/10"
								>
									Logout
								</button>
							</form>
						</div>
					{/if}
				</div>

				<form method="POST" action="/logout" class="m-0 sm:hidden">
					<input type="hidden" name="_csrf" value={csrfToken} />
					<button
						type="submit"
						class="inline-flex items-center rounded-[16px] border border-black/8 bg-white/70 px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.1em] text-zinc-900 shadow-[0_8px_24px_rgba(15,23,42,0.05),inset_0_1px_0_rgba(255,255,255,0.8)] transition-all duration-300 hover:-translate-y-0.5 hover:border-black/12 hover:bg-white dark:border-white/10 dark:bg-white/[0.05] dark:text-white"
					>
						Logout
					</button>
				</form>
			{:else}
				<div class="flex items-center gap-2">
					<a
						href="/login"
						class="inline-flex items-center rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.1em] text-zinc-700 transition-all duration-300 hover:-translate-y-0.5 hover:border-black/12 hover:bg-black/[0.06] hover:text-zinc-950 dark:border-white/10 dark:bg-white/[0.03] dark:text-zinc-300 dark:hover:border-white/20 dark:hover:bg-white/[0.06] dark:hover:text-white"
					>
						Login
					</a>

					<a
						href="/register"
						class="inline-flex items-center rounded-[16px] border border-black/8 bg-[linear-gradient(135deg,rgba(14,165,233,0.95),rgba(168,85,247,0.95))] px-4 py-2.5 text-[12px] font-semibold uppercase tracking-[0.1em] text-white shadow-[0_12px_30px_rgba(59,130,246,0.18)] transition-all duration-300 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(59,130,246,0.24)] dark:border-white/10"
					>
						Register
					</a>
				</div>
			{/if}
		</div>
	</div>

	{#if mobileMenuOpen}
		<div class="lg:hidden">
			<div
				class="fixed inset-0 z-40 bg-black/20 backdrop-blur-[2px] dark:bg-black/40"
				onclick={() => (mobileMenuOpen = false)}
			></div>

			<div class="fixed inset-x-4 top-[88px] z-50 overflow-hidden rounded-[26px] border border-black/8 bg-white/95 p-3 shadow-[0_24px_60px_rgba(15,23,42,0.16),inset_0_1px_0_rgba(255,255,255,0.95)] backdrop-blur-xl dark:border-white/10 dark:bg-[rgba(12,14,20,0.94)] dark:shadow-[0_24px_60px_rgba(0,0,0,0.38),inset_0_1px_0_rgba(255,255,255,0.05)]">
				<div class="mb-2 px-2 pb-2 pt-1 text-[11px] font-medium uppercase tracking-[0.14em] text-zinc-500">
					Navigation
				</div>

				<div class="grid gap-1">
					{#each navItems as item}
						<a
							href={item.href}
							onclick={() => (mobileMenuOpen = false)}
							class={`rounded-[18px] px-4 py-3 text-sm font-semibold transition ${
								isActive(item.href)
									? 'border border-black/8 bg-black/[0.05] text-zinc-950 dark:border-white/15 dark:bg-white/[0.10] dark:text-white'
									: 'text-zinc-700 hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white'
							}`}
						>
							{item.label}
						</a>
					{/each}

					{#if user}
						<a
							href="/settings/security"
							onclick={() => (mobileMenuOpen = false)}
							class={`rounded-[18px] px-4 py-3 text-sm font-semibold transition ${
								isActive('/settings/security')
									? 'border border-black/8 bg-black/[0.05] text-zinc-950 dark:border-white/15 dark:bg-white/[0.10] dark:text-white'
									: 'text-zinc-700 hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white'
							}`}
						>
							Sécurité
						</a>
					{/if}

					{#if user?.is_admin}
						<a
							href="/admin"
							onclick={() => (mobileMenuOpen = false)}
							class={`rounded-[18px] px-4 py-3 text-sm font-semibold transition ${
								isActive('/admin')
									? 'border border-black/8 bg-black/[0.05] text-zinc-950 dark:border-white/15 dark:bg-white/[0.10] dark:text-white'
									: 'text-zinc-700 hover:bg-black/[0.04] hover:text-zinc-950 dark:text-zinc-300 dark:hover:bg-white/[0.05] dark:hover:text-white'
							}`}
						>
							Admin
						</a>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</header>