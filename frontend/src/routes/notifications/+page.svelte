<script lang="ts">
	let { data, form } = $props();

	const { notifications, unreadCount, onlyUnread, csrfToken } = data;

	function formatDate(value: string) {
		return new Intl.DateTimeFormat('fr-FR', {
			dateStyle: 'medium',
			timeStyle: 'short'
		}).format(new Date(value));
	}
</script>

<svelte:head>
	<title>Notifications | SSD</title>
</svelte:head>

<div class="mx-auto max-w-5xl px-4 py-8">
	<div class="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
		<div>
			<p class="text-sm font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
				Compte
			</p>
			<h1 class="mt-2 text-3xl font-semibold text-zinc-900 dark:text-zinc-100">
				Notifications
			</h1>
			<p class="mt-3 text-sm text-zinc-600 dark:text-zinc-300">
				{unreadCount} non lue{unreadCount > 1 ? 's' : ''}.
			</p>
		</div>

		<div class="flex flex-wrap gap-3">
			<a
				href="/settings/notifications"
				class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				Préférences
			</a>

			<a
				href={onlyUnread ? '/notifications' : '/notifications?unread=1'}
				class="inline-flex rounded-2xl border border-zinc-300 px-5 py-3 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
			>
				{onlyUnread ? 'Voir toutes' : 'Voir non lues'}
			</a>

			<form method="POST" action="?/markAllRead">
				<input type="hidden" name="_csrf" value={csrfToken} />
				<button
					type="submit"
					class="inline-flex rounded-2xl bg-zinc-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
				>
					Tout marquer comme lu
				</button>
			</form>
		</div>
	</div>

	{#if form?.error}
		<div class="mb-4 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300">
			{form.error}
		</div>
	{/if}

	<div class="space-y-4">
		{#if notifications.length > 0}
			{#each notifications as notification}
				<section class={`rounded-3xl border p-5 shadow-sm ${
					notification.is_read
						? 'border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-950/60'
						: 'border-blue-200 bg-blue-50/60 dark:border-blue-900/50 dark:bg-blue-950/20'
				}`}>
					<div class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
						<div class="min-w-0 flex-1">
							<div class="flex flex-wrap items-center gap-2">
								{#if !notification.is_read}
									<span class="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700 dark:bg-blue-950/40 dark:text-blue-300">
										Nouveau
									</span>
								{/if}

								<span class="text-xs text-zinc-500 dark:text-zinc-400">
									{formatDate(notification.created_at)}
								</span>
							</div>

							<h2 class="mt-3 text-lg font-semibold text-zinc-900 dark:text-zinc-100">
								{notification.title}
							</h2>

							{#if notification.message}
								<p class="mt-2 text-sm leading-6 text-zinc-600 dark:text-zinc-300">
									{notification.message}
								</p>
							{/if}

							{#if notification.actor}
								<p class="mt-3 text-xs text-zinc-500 dark:text-zinc-400">
									Acteur : {notification.actor.email}
								</p>
							{/if}
						</div>

						<div class="flex w-full shrink-0 flex-wrap gap-2 md:w-auto">
							{#if notification.link}
								<a
									href={notification.link}
									class="inline-flex rounded-2xl border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-200 dark:hover:bg-zinc-800"
								>
									Ouvrir
								</a>
							{/if}

							{#if !notification.is_read}
								<form method="POST" action="?/markRead">
									<input type="hidden" name="_csrf" value={csrfToken} />
									<input type="hidden" name="notification_id" value={notification.id} />
									<button
										type="submit"
										class="inline-flex rounded-2xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-700 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
									>
										Marquer comme lue
									</button>
								</form>
							{/if}
						</div>
					</div>
				</section>
			{/each}
		{:else}
			<div class="rounded-3xl border border-dashed border-zinc-300 bg-zinc-50 p-6 text-sm text-zinc-600 dark:border-zinc-700 dark:bg-zinc-900/50 dark:text-zinc-300">
				Aucune notification.
			</div>
		{/if}
	</div>
</div>