<script lang="ts">
	let { data, form } = $props();
</script>

<svelte:head>
	<title>Connexion</title>
</svelte:head>

<section style="max-width:640px; margin:0 auto; padding:2rem 1rem 4rem;">
	<div
		style="border:1px solid rgba(255,255,255,0.08); border-radius:28px; background:linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); padding:2rem; box-shadow:0 20px 60px rgba(0,0,0,0.28);"
	>
		<h1 style="margin-top:0;">Connexion</h1>
		<p style="color:#cbd5e1; line-height:1.7;">
			Connecte-toi à ton espace pour accéder à l’App Store, à tes serveurs et à tes
			installations.
		</p>

		<form method="POST" style="display:grid; gap:1rem; margin-top:1.25rem;">
			<input type="hidden" name="_csrf" value={data.csrfToken} />

			<label style="display:grid; gap:0.5rem;">
				<span>Email</span>
				<input
					name="email"
					type="email"
					value={form?.email ?? ''}
					placeholder="you@example.com"
					style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
				/>
			</label>

			<label style="display:grid; gap:0.5rem;">
				<span>Mot de passe</span>
				<input
					name="password"
					type="password"
					placeholder="••••••••••••"
					style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
				/>
			</label>

			<label style="display:grid; gap:0.5rem;">
				<span>Code 2FA</span>
				<input
					name="otp_code"
					type="text"
					inputmode="numeric"
					autocomplete="one-time-code"
					value={form?.otp_code ?? ''}
					placeholder="À renseigner seulement si le 2FA est activé sur le compte."
					style="padding:0.95rem 1rem; border-radius:16px; border:1px solid rgba(255,255,255,0.08); background:rgba(15,23,42,0.6); color:white;"
				/>
			</label>

			<button
				type="submit"
				style="padding:0.95rem 1rem; border:none; border-radius:16px; font-weight:700; cursor:pointer; background:linear-gradient(90deg, #38bdf8, #2563eb); color:white;"
			>
				Se connecter
			</button>
		</form>

		{#if form?.error}
			<p style="color:#fca5a5; margin-top:1rem;">{form.error}</p>
		{/if}

		<p style="margin-top:1.25rem; color:#cbd5e1;">
			Pas encore de compte ? <a href="/register" style="color:#93c5fd;">Créer un compte</a>
		</p>
	</div>
</section>