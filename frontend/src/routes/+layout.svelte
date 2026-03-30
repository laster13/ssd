<script lang="ts">
	let { data, children } = $props();
</script>

<nav
	style="display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:1rem 1.25rem; border-bottom:1px solid rgba(255,255,255,0.08); background:rgba(10,14,24,0.7); backdrop-filter: blur(16px); position:sticky; top:0; z-index:20;"
>
	<div style="display:flex; align-items:center; gap:1rem;">
		<a href="/app-store" style="font-weight:700; text-decoration:none; color:white;">SSD</a>
		<a href="/app-store" style="text-decoration:none; color:#cbd5e1;">App Store</a>
		<a href="/servers" style="text-decoration:none; color:#cbd5e1;">Serveurs</a>
		<a href="/installations" style="text-decoration:none; color:#cbd5e1;">Installations</a>

		{#if data.user}
			<a href="/settings/security" style="text-decoration:none; color:#cbd5e1;">Sécurité</a>
		{/if}

		{#if data.user?.is_admin}
			<a href="/admin" style="text-decoration:none; color:#64748b;">Admin</a>
		{/if}
	</div>

	<div style="display:flex; align-items:center; gap:1rem;">
		{#if data.user}
			<span style="color:#94a3b8;">Connecté : {data.user.email}</span>
			<a href="/logout" style="text-decoration:none; color:white;">Logout</a>
		{:else}
			<a href="/login" style="text-decoration:none; color:white;">Login</a>
			<a href="/register" style="text-decoration:none; color:white;">Register</a>
		{/if}
	</div>
</nav>

<div
	style="min-height:100vh; background:
	radial-gradient(circle at top left, rgba(56,189,248,0.18), transparent 32%),
	radial-gradient(circle at top right, rgba(168,85,247,0.16), transparent 28%),
	radial-gradient(circle at bottom center, rgba(16,185,129,0.12), transparent 24%),
	linear-gradient(180deg, #060816 0%, #0b1020 100%);
	color:white;"
>
	<div style="max-width:1280px; margin:0 auto; padding:1.5rem;">
		{@render children()}
	</div>
</div>