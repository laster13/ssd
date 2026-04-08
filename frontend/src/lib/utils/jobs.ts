export type JobStatus = 'pending' | 'claimed' | 'running' | 'completed' | 'failed';
export type HistoryFilter = 'all' | 'running' | 'completed' | 'failed';

export type Job = {
	id: string;
	machine_id: string;
	type?: string;
	status: string;
	created_at?: string;
	updated_at?: string;
	payload?: {
		app_slug?: string;
		app_name?: string;
	};
};

export type Machine = {
	id: string;
	hostname?: string;
	machine_uuid?: string;
	status?: string;
};

export type ApplicationTransition = 'idle' | 'installing' | 'uninstalling';

export type ApplicationState = {
	id: string;
	machine_id: string;
	app_slug: string;
	app_name?: string | null;
	present: boolean;
	transition: ApplicationTransition;
	last_operation?: 'install' | 'uninstall' | null;
	last_job_id?: string | null;
	last_job_status?: string | null;
	last_error?: string | null;
	installed_at?: string | null;
	created_at?: string;
	updated_at?: string;
	public_url?: string | null;
};

export type JobStatusVariant = 'applications' | 'history';

export function appName(job: Job) {
	return job?.payload?.app_name ?? job?.payload?.app_slug ?? 'Application';
}

export function appSlug(job: Job) {
	return job?.payload?.app_slug ?? 'unknown';
}

export function humanJobStatus(status: string, variant: JobStatusVariant = 'history') {
	if (variant === 'applications') {
		switch (status) {
			case 'pending':
				return 'En attente';
			case 'claimed':
				return 'Prise en charge';
			case 'running':
				return 'Déploiement';
			case 'completed':
				return 'En ligne';
			case 'failed':
				return 'Incident';
			default:
				return status;
		}
	}

	switch (status) {
		case 'pending':
			return 'En attente';
		case 'claimed':
			return 'Préparation';
		case 'running':
			return 'En cours';
		case 'completed':
			return 'Terminée';
		case 'failed':
			return 'Échec';
		default:
			return status;
	}
}

export function jobStatusClass(status: string) {
	switch (status) {
		case 'completed':
			return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/8 dark:text-emerald-300';
		case 'failed':
			return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/8 dark:text-rose-300';
		case 'running':
			return 'border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-400/15 dark:bg-cyan-500/8 dark:text-cyan-300';
		case 'claimed':
			return 'border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-400/15 dark:bg-indigo-500/8 dark:text-indigo-300';
		case 'pending':
			return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/15 dark:bg-amber-500/8 dark:text-amber-300';
		default:
			return 'border-zinc-200 bg-zinc-100 text-zinc-600 dark:border-white/10 dark:bg-white/[0.05] dark:text-zinc-300';
	}
}

export function jobStatusDotClass(status: string) {
	switch (status) {
		case 'completed':
			return 'bg-emerald-500 dark:bg-emerald-400';
		case 'failed':
			return 'bg-rose-500 dark:bg-rose-400';
		case 'running':
			return 'bg-cyan-500 dark:bg-cyan-400';
		case 'claimed':
			return 'bg-indigo-500 dark:bg-indigo-400';
		case 'pending':
			return 'bg-amber-500 dark:bg-amber-400';
		default:
			return 'bg-zinc-400 dark:bg-zinc-500';
	}
}

export function formatFrenchDate(value?: string | null) {
	if (!value) return '-';
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return value;

	return new Intl.DateTimeFormat('fr-FR', {
		day: '2-digit',
		month: 'long',
		year: 'numeric'
	}).format(date);
}

export function formatFrenchDateTime(value?: string | null) {
	if (!value) return '—';
	const date = new Date(value);
	if (Number.isNaN(date.getTime())) return value;

	return new Intl.DateTimeFormat('fr-FR', {
		dateStyle: 'medium',
		timeStyle: 'short'
	}).format(date);
}

export function machineStatusLabel(status?: string) {
	switch (status) {
		case 'online':
			return 'En ligne';
		case 'offline':
			return 'Hors ligne';
		case 'provisioning':
			return 'Provisionnement';
		case 'maintenance':
			return 'Maintenance';
		default:
			return status || 'Inconnu';
	}
}

export function machinePillClass(status?: string) {
	switch (status) {
		case 'online':
			return 'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-400/15 dark:bg-emerald-500/8 dark:text-emerald-300';
		case 'offline':
			return 'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-400/15 dark:bg-rose-500/8 dark:text-rose-300';
		case 'maintenance':
			return 'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-400/15 dark:bg-amber-500/8 dark:text-amber-300';
		default:
			return 'border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-white/10 dark:bg-white/[0.04] dark:text-zinc-300';
	}
}

export function matchesHistoryFilter(job: Pick<Job, 'status'>, filter: HistoryFilter) {
	if (filter === 'all') return true;
	if (filter === 'completed') return job.status === 'completed';
	if (filter === 'failed') return job.status === 'failed';
	if (filter === 'running') {
		return ['pending', 'claimed', 'running'].includes(job.status);
	}
	return true;
}

export function historyFilterLabel(filter: HistoryFilter) {
	switch (filter) {
		case 'running':
			return 'En cours';
		case 'completed':
			return 'En ligne';
		case 'failed':
			return 'Incidents';
		default:
			return 'Toutes';
	}
}