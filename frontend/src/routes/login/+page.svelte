<script lang="ts">
	let { data, form } = $props();
</script>

<svelte:head>
	<title>Connexion</title>
</svelte:head>

<section class="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
	<div class="overflow-hidden rounded-[30px] border border-black/5 bg-white/70 shadow-[0_20px_80px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-white/[0.035] dark:shadow-[0_20px_80px_rgba(0,0,0,0.28)]">
		<div class="relative">
			<div class="pointer-events-none absolute inset-0 bg-[linear-gradient(to_bottom,rgba(255,255,255,0.78),rgba(255,255,255,0.45))] dark:bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.03))]"></div>

			<div class="relative p-6 sm:p-8">
				<div class="mb-6">
					<div class="mb-3 inline-flex items-center gap-2 rounded-full border border-black/5 bg-black/[0.03] px-3 py-1.5 text-[11px] font-medium uppercase tracking-[0.16em] text-zinc-600 dark:border-white/10 dark:bg-white/[0.045] dark:text-zinc-300">
						<span class="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
						Connexion
					</div>

					<h1 class="text-3xl font-semibold tracking-[-0.05em] text-zinc-950 dark:text-white sm:text-4xl">
						Connexion
					</h1>

					<p class="mt-3 max-w-2xl text-sm leading-7 text-zinc-600 dark:text-zinc-400 sm:text-base">
						Connecte-toi à ton espace pour accéder à l’App Store, à tes serveurs et à
						tes installations.
					</p>
				</div>

				<form method="POST" class="grid gap-4">
					<input type="hidden" name="_csrf" value={data.csrfToken} />

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">Email</span>
						<input
							name="email"
							type="email"
							value={form?.email ?? ''}
							placeholder="you@example.com"
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						/>
					</label>

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">
							Mot de passe
						</span>
						<input
							name="password"
							type="password"
							placeholder="••••••••••••"
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						/>
					</label>

					<label class="grid gap-2">
						<span class="text-sm font-medium text-zinc-800 dark:text-zinc-200">Code 2FA</span>
						<input
							name="otp_code"
							type="text"
							inputmode="numeric"
							autocomplete="one-time-code"
							value={form?.otp_code ?? ''}
							placeholder="À renseigner seulement si le 2FA est activé sur le compte."
							class="rounded-[16px] border border-black/8 bg-black/[0.03] px-4 py-4 text-zinc-900 placeholder:text-zinc-500 outline-none transition-all duration-200 focus:border-black/12 focus:bg-black/[0.05] dark:border-white/10 dark:bg-[rgba(15,23,42,0.6)] dark:text-white dark:placeholder:text-zinc-500 dark:focus:border-white/20 dark:focus:bg-[rgba(15,23,42,0.72)]"
						/>
					</label>

					<button
						type="submit"
						class="mt-2 inline-flex items-center justify-center rounded-[16px] border border-cyan-200 bg-[linear-gradient(90deg,#38bdf8,#2563eb)] px-4 py-4 text-sm font-semibold text-white shadow-[0_12px_30px_rgba(37,99,235,0.20)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_16px_36px_rgba(37,99,235,0.26)] dark:border-white/10"
					>
						Se connecter
					</button>
				</form>

				{#if form?.error}
					<p class="mt-5 text-sm font-medium text-red-600 dark:text-red-300">{form.error}</p>
				{/if}

				<p class="mt-6 text-sm text-zinc-600 dark:text-zinc-300">
					Pas encore de compte ?
					<a
						href="/register"
						class="font-medium text-sky-600 transition hover:text-sky-700 dark:text-sky-300 dark:hover:text-sky-200"
					>
						Créer un compte
					</a>
				</p>
			</div>
		</div>
	</div>
</section>