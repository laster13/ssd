<script lang="ts">
	let { data } = $props();

	const logs = data.logs ?? [];

	function formatValue(value: unknown) {
		if (value == null) return '-';
		if (typeof value === 'object') return JSON.stringify(value, null, 2);
		return String(value);
	}

	function severityClass(severity: string) {
		switch (severity?.toLowerCase()) {
			case 'critical':
				return 'border-red-200 bg-red-50 text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300';
			case 'warning':
				return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/20 dark:bg-amber-400/10 dark:text-amber-300';
			default:
				return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300';
		}
	}

	function successClass(success: boolean) {
		return success
			? 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/20 dark:bg-emerald-400/10 dark:text-emerald-300'
			: 'border-red-200 bg-red-50 text-red-700 dark:border-red-400/20 dark:bg-red-400/10 dark:text-red-300';
	}
</script>

<svelte:head>
	<title>Audit sécurité</title>
</svelte:head>

<section class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
	<a
		href="/admin"
		class="mb-4 inline-flex items-center gap-2 text-sm font-medium text-sky-600 transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
	>
		<span>←</span>
		<span>Retour admin</span>
	</a>

	<div
		class="mb-6 overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
	>
		<div class="relative">
			<div
				class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
			></div>

			<div class="relative p-6 sm:p-8">
				<div
					class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300"
				>
					<span class="h-1.5 w-1.5 rounded-full bg-orange-400"></span>
					Sécurité
				</div>

				<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
					Audit sécurité
				</h1>

				<p class="mt-3 max-w-3xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
					Retrouve ici les événements sensibles du système : authentification, 2FA, pairing,
					création de jobs, rotation de tokens machine et révocation de machines.
				</p>
			</div>
		</div>
	</div>

	{#if logs.length > 0}
		<div class="grid gap-4">
			{#each logs as log}
				<article
					class="overflow-hidden rounded-[28px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]"
				>
					<div class="relative">
						<div
							class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"
						></div>

						<div class="relative p-5 sm:p-6">
							<div class="mb-4 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
								<div>
									<h2 class="text-lg font-semibold tracking-[-0.03em] text-zinc-950 dark:text-white">
										{log.event_type}
									</h2>
									<div class="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
										{log.created_at}
									</div>
								</div>

								<div class="flex flex-wrap gap-2">
									<div
										class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${severityClass(log.severity)}`}
									>
										{log.severity}
									</div>

									<div
										class={`inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold ${successClass(log.success)}`}
									>
										{log.success ? 'success' : 'failure'}
									</div>

									{#if log.status_code}
										<div
											class="inline-flex items-center rounded-full border border-black/8 bg-black/[0.03] px-2.5 py-1 text-xs font-semibold text-zinc-700 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300"
										>
											HTTP {log.status_code}
										</div>
									{/if}
								</div>
							</div>

							{#if log.description}
								<p class="mb-4 text-sm leading-7 text-zinc-700 dark:text-zinc-300 sm:text-[15px]">
									{log.description}
								</p>
							{/if}

							<div class="mb-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
								<div
									class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]"
								>
									<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Actor type
									</div>
									<div class="text-sm text-zinc-800 dark:text-zinc-200">
										{formatValue(log.actor_type)}
									</div>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]"
								>
									<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Actor user
									</div>
									<div class="text-sm text-zinc-800 dark:text-zinc-200">
										{formatValue(log.actor_user_id)}
									</div>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]"
								>
									<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										Target machine
									</div>
									<div class="text-sm text-zinc-800 dark:text-zinc-200">
										{formatValue(log.target_machine_id)}
									</div>
								</div>

								<div
									class="rounded-[18px] border border-black/5 bg-black/[0.025] px-4 py-4 dark:border-white/10 dark:bg-white/[0.03]"
								>
									<div class="mb-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-zinc-500 dark:text-zinc-400">
										IP
									</div>
									<div class="text-sm text-zinc-800 dark:text-zinc-200">
										{formatValue(log.ip_address)}
									</div>
								</div>
							</div>

							{#if log.details}
								<div
									class="rounded-[20px] border border-black/5 bg-white/50 p-4 dark:border-white/10 dark:bg-[rgba(2,6,23,0.5)]"
								>
									<div class="mb-3 text-sm font-medium text-zinc-700 dark:text-zinc-300">
										Details
									</div>
									<pre
										class="overflow-x-auto whitespace-pre-wrap break-words text-sm leading-6 text-zinc-600 dark:text-zinc-300"
									>{JSON.stringify(log.details, null, 2)}</pre>
								</div>
							{/if}
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div
			class="rounded-[24px] border border-dashed border-black/10 bg-black/[0.02] px-5 py-8 text-sm text-zinc-600 dark:border-white/10 dark:bg-white/[0.02] dark:text-zinc-400"
		>
			Aucun événement d’audit pour le moment.
		</div>
	{/if}
</section>