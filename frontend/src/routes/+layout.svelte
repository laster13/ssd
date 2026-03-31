<script lang="ts">
	let { data, children } = $props();
</script>

<svelte:head>
	<title>SSD</title>
</svelte:head>

<header
	style="display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1rem 1.25rem; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:1.5rem;"
>
	<nav style="display:flex; flex-wrap:wrap; gap:1rem; align-items:center;">
		<a href="/app-store" style="color:white; text-decoration:none; font-weight:700;">SSD</a>
		<a href="/app-store" style="color:#cbd5e1; text-decoration:none;">App Store</a>
		<a href="/servers" style="color:#cbd5e1; text-decoration:none;">Serveurs</a>
		<a href="/installations" style="color:#cbd5e1; text-decoration:none;">Installations</a>
		<a href="/applications" style="color:#cbd5e1; text-decoration:none;">Applications</a>

		{#if data.user}
			<a href="/settings/security" style="color:#cbd5e1; text-decoration:none;">Sécurité</a>
		{/if}

		{#if data.user?.is_admin}
			<a href="/admin" style="color:#cbd5e1; text-decoration:none;">Admin</a>
		{/if}
	</nav>

	<div style="display:flex; align-items:center; gap:0.9rem; flex-wrap:wrap;">
		{#if data.user}
			<span style="color:#94a3b8;">Connecté : {data.user.email}</span>

			<form method="POST" action="/logout" style="display:inline;">
				<input type="hidden" name="_csrf" value={data.csrfToken} />
				<button
					type="submit"
					style="padding:0.65rem 0.9rem; border-radius:12px; border:1px solid rgba(255,255,255,0.08); background:rgba(255,255,255,0.04); color:white; cursor:pointer;"
				>
					Logout
				</button>
			</form>
		{:else}
			<a href="/login" style="color:#cbd5e1; text-decoration:none;">Login</a>
			<a href="/register" style="color:#cbd5e1; text-decoration:none;">Register</a>
		{/if}
	</div>
</header>

<main style="padding:0 1rem 3rem;">
	{@render children()}
</main>