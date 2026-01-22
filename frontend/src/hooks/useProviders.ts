// ============================================
// VAULT TV - Providers Hook
// ============================================

import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db';
import type { Provider } from '../types';

export function useProviders() {
  return useLiveQuery(() => db.providers.toArray(), [], []);
}

export function useActiveProviders() {
  return useLiveQuery(() => db.getActiveProviders(), [], []);
}

export function useProvider(providerId: string | null) {
  return useLiveQuery(
    () => providerId ? db.providers.get(providerId) : Promise.resolve(undefined),
    [providerId],
    undefined
  );
}

export function useCategories(providerId: string | null, type?: 'live' | 'movie' | 'series') {
  return useLiveQuery(
    () => {
      if (!providerId) return Promise.resolve([]);
      if (type) {
        return db.categories.where('[providerId+type]').equals([providerId, type]).toArray();
      }
      return db.categories.where('providerId').equals(providerId).toArray();
    },
    [providerId, type],
    []
  );
}

export default useProviders;
