<script lang="ts">
	let { data, form } = $props();

	type AdminUser = {
		id: string;
		email: string;
		is_active: boolean;
		is_admin: boolean;
		created_at?: string;
		updated_at?: string;
	};

	type UserFilter = 'all' | 'admins' | 'eligible' | 'inactive';

	let activeFilter = $state<UserFilter>('all');
	let searchQuery = $state('');

	const users = $derived((data.users ?? []) as AdminUser[]);

	const counts = $derived.by(() => ({
		total: users.length,
		admins: users.filter((user) => user.is_admin).length,
		eligible: users.filter((user) => user.is_active && !user.is_admin).length,
		inactive: users.filter((user) => !user.is_active).length
	}));

	const filteredUsers = $derived.by(() => {
		const query = searchQuery.trim().toLowerCase();

		return users
			.filter((user) => {
				if (activeFilter === 'admins') return user.is_admin;
				if (activeFilter === 'eligible') return user.is_active && !user.is_admin;
				if (activeFilter === 'inactive') return !user.is_active;
				return true;
			})
			.filter((user) => {
				if (!query) return true;
				return user.email.toLowerCase().includes(query);
			})
			.sort((a, b) => {
				const aTime = a.updated_at ? new Date(a.updated_at).getTime() : 0;
				const bTime = b.updated_at ? new Date(b.updated_at).getTime() : 0;
				return bTime - aTime;
			});
	});

	function setFilter(filter: UserFilter) {
		activeFilter = filter;
	}

	function formatDate(value?: string | null) {
		if (!value) return '—';

		const date = new Date(value);
		if (Number.isNaN(date.getTime())) return value;

		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(date);
	}

	function roleLabel(user: AdminUser) {
		if (user.is_admin) return 'Admin';
		if (!user.is_active) return 'Inactif';
		return 'Standard';
	}

	function roleClass(user: AdminUser) {
		if (user.is_admin) {
			return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/8 dark:text-emerald-300';
		}

		if (!user.is_active) {
			return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/8 dark:text-rose-300';
		}

		return 'border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-400/15 dark:bg-cyan-500/8 dark:text-cyan-300';
	}

	function cardClass(active: boolean) {
		return active
			? 'border-cyan-200 shadow-[0_20px_60px_rgba(37,99,235,0.14)] dark:border-cyan-400/20'
			: 'border-black/5 hover:border-black/10 dark:border-white/10 dark:hover:border-white/14';
	}
</script>

<svelte:head>
	<title>Admin — Utilisateurs</title>
</svelte:head>

<section class="relative isolate overflow-hidden">
	<div class="pointer-events-none absolute inset-0 -z-30 bg-[linear-gradient(180deg,#f8fafc_0%,#eef2ff_24%,#f8fafc_50%,#ecfeff_100%)] dark:bg-[linear-gradient(180deg,#050816_0%,#0b1020_38%,#0a1120_68%,#07111f_100%)]"></div>

	<div class="pointer-events-none absolute inset-0 -z-20 opacity-90">
		<div class="absolute left-[-8rem] top-[-7rem] h-[28rem] w-[28rem] rounded-full bg-cyan-400/18 blur-3xl dark:bg-cyan-400/16"></div>
		<div class="absolute right-[-10rem] top-[-5rem] h-[32rem] w-[32rem] rounded-full bg-fuchsia-400/14 blur-3xl dark:bg-fuchsia-500/14"></div>
		<div class="absolute bottom-[-12rem] left-[12%] h-[26rem] w-[26rem] rounded-full bg-emerald-400/14 blur-3xl dark:bg-emerald-400/12"></div>
	</div>

	<div class="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.9),transparent_24%),radial-gradient(circle_at_80%_0%,rgba(125,211,252,0.18),transparent_22%),radial-gradient(circle_at_20%_100%,rgba(52,211,153,0.14),transparent_18%)] dark:bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.06),transparent_20%),radial-gradient(circle_at_82%_0%,rgba(56,189,248,0.14),transparent_22%),radial-gradient(circle_at_18%_100%,rgba(16,185,129,0.12),transparent_18%)]"></div>

	<div class="mx-auto max-w-7xl px-4 pb-8 pt-8 sm:px-6 lg:px-8 lg:pt-12">
		<div class="relative overflow-hidden rounded-[38px] border border-black/5 bg-white/75 shadow-[0_35px_120px_rgba(15,23,42,0.10)] backdrop-blur-3xl dark:border-white/10 dark:bg-white/[0.05] dark:shadow-[0_35px_120px_rgba(0,0,0,0.45)]">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.90),rgba(255,255,255,0.62)_42%,rgba(255,255,255,0.50)_100%)] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.07),rgba(255,255,255,0.03)_45%,rgba(255,255,255,0.02)_100%)]"></div>
			<div class="pointer-events-none absolute inset-0 rounded-[38px] ring-1 ring-inset ring-white/70 dark:ring-white/10"></div>

			<div class="relative p-6 sm:p-8 lg:p-10">
				<p class="mb-5">
					<a
						href="/admin"
						class="inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/70 px-3 py-2 text-sm font-medium text-zinc-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.82)] transition hover:border-black/10 hover:bg-white dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-200 dark:hover:border-white/14 dark:hover:bg-white/[0.06]"
					>
						← Retour à l’administration
					</a>
				</p>

                                <div class="flex flex-col gap-6 xl:flex-row xl:items-start xl:justify-between">
                                      <div class="max-w-3xl">
                                              <div class="mb-4 flex flex-wrap items-center gap-3">
                                                      <div
                                                      	class="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50/90 px-3.5 py-2 text-[11px] font-semibold uppercase tracking-[0.24em] text-emerald-700 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.06] dark:text-emerald-200"
                                                      >
                                                      	<span
                                                      		class="inline-block h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_16px_rgba(16,185,129,0.55)] dark:bg-emerald-400 dark:shadow-[0_0_14px_rgba(52,211,153,0.65)]"
                                                      	></span>
                                                      	Admin users
                                                      </div>

                                                      <div
                                                      	class="inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/70 px-3 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-zinc-600 shadow-[inset_0_1px_0_rgba(255,255,255,0.85)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300"
                                                      >
                                                      	Gestion dédiée
                                                      </div>
                                              </div>

                                              <h1
                                              	class="max-w-2xl text-lg font-semibold tracking-[-0.04em] text-zinc-950 dark:text-zinc-50 sm:text-xl xl:text-2xl xl:leading-[1.1]"
                                              >
                                                      <span
                                                      	class="block bg-[linear-gradient(90deg,#0f172a_0%,#0891b2_18%,#059669_44%,#2563eb_70%,#7c3aed_100%)] bg-clip-text text-transparent dark:bg-[linear-gradient(90deg,#f8fafc_0%,#a7f3d0_18%,#67e8f9_40%,#93c5fd_66%,#d8b4fe_100%)]"
                                                      >
                                                      	Gestion Utilisateurs
                                                      </span>
                                              </h1>

                                              <p class="mt-3 max-w-xl text-sm leading-7 text-zinc-600 dark:text-zinc-400">
                                                      Recherche, filtrage et actions d’administration dans une vue dédiée.
                                              </p>
                                      </div>

                                      <div class="w-full xl:max-w-xl xl:pt-1">
                                              <div
                                              	class="relative overflow-hidden rounded-[28px] border border-black/5 bg-white/72 p-4 shadow-[0_20px_60px_rgba(15,23,42,0.10)] backdrop-blur-2xl dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_20px_60px_rgba(0,0,0,0.32)]"
                                              >
                                              	<div
                                              		class="pointer-events-none absolute inset-0 bg-[linear-gradient(135deg,rgba(255,255,255,0.82),rgba(255,255,255,0.55))] dark:bg-[linear-gradient(135deg,rgba(255,255,255,0.05),rgba(255,255,255,0.02))]"
                                              	></div>

                                              	<div class="relative">
                                                      <p
                                                      	class="text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 dark:text-zinc-400"
                                                      >
                                                      	Recherche rapide
                                                      </p>

                                                      <input
                                                      	bind:value={searchQuery}
                                                      	type="search"
                                                      	placeholder="Rechercher par email"
                                                      	class="mt-3 w-full rounded-[18px] border border-black/8 bg-black/[0.03] px-4 py-3 text-sm text-zinc-900 outline-none transition placeholder:text-zinc-500 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-white/[0.04] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/16 dark:focus:bg-white/[0.06]"
                                                      />

                                                      <p class="mt-3 text-sm text-zinc-500 dark:text-zinc-400">
                                                      	{filteredUsers.length} résultat(s) affiché(s)
                                                      </p>
                                              	</div>
                                              </div>
                                      </div>
                                </div>

				{#if form?.success}
					<div class="mt-6 rounded-[20px] border border-emerald-200 bg-emerald-50/85 px-4 py-4 text-sm font-medium text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/10 dark:text-emerald-300">
						Action admin exécutée avec succès.
					</div>
				{/if}

				{#if form?.error}
					<div class="mt-6 rounded-[20px] border border-rose-200 bg-rose-50/85 px-4 py-4 text-sm font-medium text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/10 dark:text-rose-300">
						{form.error}
					</div>
				{/if}
			</div>
		</div>
	</div>
</section>

<section class="mx-auto max-w-7xl px-4 pb-14 sm:px-6 lg:px-8">
	<div class="mb-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
		<button type="button" onclick={() => setFilter('all')} class={`group relative overflow-hidden rounded-[28px] border bg-white/78 p-5 text-left shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(15,23,42,0.12)] dark:bg-white/[0.045] dark:shadow-[0_20px_60px_rgba(0,0,0,0.30)] ${cardClass(activeFilter === 'all')}`}>
			<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-zinc-500 dark:text-zinc-400">Total</div>
			<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">{counts.total}</div>
			<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Comptes utilisateurs</div>
		</button>

		<button type="button" onclick={() => setFilter('admins')} class={`group relative overflow-hidden rounded-[28px] border bg-emerald-50/85 p-5 text-left shadow-[0_20px_60px_rgba(16,185,129,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(16,185,129,0.16)] dark:bg-emerald-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)] ${activeFilter === 'admins' ? 'border-emerald-300 dark:border-emerald-400/20' : 'border-emerald-200/70 dark:border-emerald-400/15'}`}>
			<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-emerald-700 dark:text-emerald-200/90">Admins</div>
			<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">{counts.admins}</div>
			<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Droits déjà actifs</div>
		</button>

		<button type="button" onclick={() => setFilter('eligible')} class={`group relative overflow-hidden rounded-[28px] border bg-cyan-50/85 p-5 text-left shadow-[0_20px_60px_rgba(14,165,233,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(14,165,233,0.16)] dark:bg-cyan-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)] ${activeFilter === 'eligible' ? 'border-cyan-300 dark:border-cyan-400/20' : 'border-cyan-200/70 dark:border-cyan-400/15'}`}>
			<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-cyan-700 dark:text-cyan-200/90">Utilisateurs</div>
			<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">{counts.eligible}</div>
			<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Actifs et non-admin</div>
		</button>

		<button type="button" onclick={() => setFilter('inactive')} class={`group relative overflow-hidden rounded-[28px] border bg-rose-50/85 p-5 text-left shadow-[0_20px_60px_rgba(244,63,94,0.10)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:shadow-[0_28px_70px_rgba(244,63,94,0.16)] dark:bg-rose-500/[0.08] dark:shadow-[0_20px_60px_rgba(0,0,0,0.26)] ${activeFilter === 'inactive' ? 'border-rose-300 dark:border-rose-400/20' : 'border-rose-200/70 dark:border-rose-400/15'}`}>
			<div class="text-[11px] font-semibold uppercase tracking-[0.24em] text-rose-700 dark:text-rose-200/90">Inactifs</div>
			<div class="mt-5 text-4xl font-bold tracking-[-0.07em] text-zinc-950 dark:text-zinc-50">{counts.inactive}</div>
			<div class="mt-2 text-sm text-zinc-500 dark:text-zinc-400">Compte désactivé</div>
		</button>
	</div>

	{#if filteredUsers.length > 0}
		<div class="grid grid-cols-1 gap-6 xl:grid-cols-2">
			{#each filteredUsers as user}
				<article class="group relative overflow-hidden rounded-[30px] border border-black/5 bg-white/82 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.09)] backdrop-blur-2xl transition duration-300 hover:-translate-y-1 hover:border-black/10 hover:shadow-[0_32px_85px_rgba(15,23,42,0.14)] dark:border-white/10 dark:bg-white/[0.045] dark:shadow-[0_24px_70px_rgba(0,0,0,0.34)] dark:hover:border-white/14 dark:hover:bg-white/[0.055]">
					<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(180deg,rgba(255,255,255,0.86),rgba(255,255,255,0.58)_42%,rgba(255,255,255,0.46))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.025)_42%,rgba(255,255,255,0.015))]"></div>
					<div class="relative">
						<div class="mb-5 flex items-start justify-between gap-4">
							<div class="min-w-0">
								<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-white/75 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-zinc-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-400">
									Compte
								</div>

								<h2 class="truncate text-[1.2rem] font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50 sm:text-[1.35rem]">
									{user.email}
								</h2>
							</div>

							<span class={`inline-flex rounded-full border px-3 py-1.5 text-[11px] font-semibold uppercase tracking-[0.14em] shadow-[0_10px_24px_rgba(15,23,42,0.08),inset_0_1px_0_rgba(255,255,255,0.78)] backdrop-blur-xl dark:shadow-[0_10px_24px_rgba(0,0,0,0.24),inset_0_1px_0_rgba(255,255,255,0.04)] ${roleClass(user)}`}>
								{roleLabel(user)}
							</span>
						</div>

						<div class="rounded-[22px] border border-black/5 bg-white/72 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/10 dark:bg-white/[0.03] dark:shadow-[inset_0_1px_0_rgba(255,255,255,0.03)]">
							<div class="mb-4 text-[11px] font-semibold uppercase tracking-[0.2em] text-zinc-500 dark:text-zinc-400">
								Détails
							</div>

							<dl class="space-y-3">
								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Email</dt>
									<dd class="max-w-[65%] break-all text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{user.email}
									</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Créé le</dt>
									<dd class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{formatDate(user.created_at)}
									</dd>
								</div>

								<div class="flex items-start justify-between gap-4">
									<dt class="text-sm text-zinc-500">Dernière mise à jour</dt>
									<dd class="max-w-[65%] text-right text-sm font-semibold text-zinc-950 dark:text-zinc-100">
										{formatDate(user.updated_at)}
									</dd>
								</div>
							</dl>
						</div>

						<div class="mt-5 grid gap-3 sm:grid-cols-2">
							{#if user.is_admin}
								<form method="POST" action="?/revokeAdmin">
									<input type="hidden" name="_csrf" value={data.csrfToken} />
									<input type="hidden" name="user_id" value={user.id} />

									<button
										type="submit"
										class="inline-flex w-full items-center justify-center rounded-[18px] border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-semibold text-amber-700 transition hover:bg-amber-100 dark:border-amber-400/15 dark:bg-amber-500/10 dark:text-amber-300 dark:hover:bg-amber-500/16"
									>
										Rétrograder admin
									</button>
								</form>
							{:else if user.is_active}
								<form method="POST" action="?/grantAdmin">
									<input type="hidden" name="_csrf" value={data.csrfToken} />
									<input type="hidden" name="user_id" value={user.id} />

									<button
										type="submit"
										class="relative inline-flex w-full items-center justify-center overflow-hidden rounded-[20px] border border-cyan-200 px-4 py-3 text-sm font-semibold text-white shadow-[0_16px_36px_rgba(37,99,235,0.24)] transition duration-200 hover:scale-[1.01] hover:shadow-[0_20px_40px_rgba(37,99,235,0.30)] dark:border-cyan-400/15 dark:shadow-[0_16px_34px_rgba(0,0,0,0.30)]"
									>
										<span class="absolute inset-0 bg-[linear-gradient(135deg,rgba(14,165,233,0.98),rgba(37,99,235,0.96),rgba(124,58,237,0.92))]"></span>
										<span class="absolute inset-0 opacity-80 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.24),transparent_55%)]"></span>
										<span class="relative">Promouvoir admin</span>
									</button>
								</form>
							{:else}
								<div class="rounded-[18px] border border-rose-200 bg-rose-50/85 px-4 py-3 text-sm font-medium text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/10 dark:text-rose-300">
									Compte inactif
								</div>
							{/if}

							<form method="POST" action="?/deleteUser">
								<input type="hidden" name="_csrf" value={data.csrfToken} />
								<input type="hidden" name="user_id" value={user.id} />

								<button
									type="submit"
									class="inline-flex w-full items-center justify-center rounded-[18px] border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-700 transition hover:bg-rose-100 dark:border-rose-400/15 dark:bg-rose-500/10 dark:text-rose-300 dark:hover:bg-rose-500/16"
								>
									Supprimer le compte
								</button>
							</form>
						</div>
					</div>
				</article>
			{/each}
		</div>
	{:else}
		<div class="relative overflow-hidden rounded-[30px] border border-black/5 bg-white/80 p-8 shadow-[0_20px_60px_rgba(15,23,42,0.08)] backdrop-blur-xl dark:border-white/8 dark:bg-white/[0.03] dark:shadow-[0_20px_60px_rgba(0,0,0,0.28)]">
			<div class="relative mx-auto max-w-xl text-center">
				<div class="mx-auto flex h-16 w-16 items-center justify-center rounded-[22px] border border-black/5 bg-white text-2xl shadow-[inset_0_1px_0_rgba(255,255,255,0.8)] dark:border-white/8 dark:bg-white/[0.04] dark:shadow-none">
					✦
				</div>

				<h2 class="mt-5 text-2xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-zinc-50">
					Aucun utilisateur pour ce filtre
				</h2>

				<p class="mt-3 text-base leading-7 text-zinc-600 dark:text-zinc-400">
					Essaie un autre filtre ou ajuste la recherche email.
				</p>
			</div>
		</div>
	{/if}
</section>