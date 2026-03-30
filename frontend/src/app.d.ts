declare global {
	namespace App {
		interface Locals {
			token: string | null;
			user: {
				id: string;
				email: string;
				is_admin: boolean;
			} | null;
		}

		interface PageData {
			user: {
				id: string;
				email: string;
				is_admin: boolean;
			} | null;
		}
	}
}

export {};