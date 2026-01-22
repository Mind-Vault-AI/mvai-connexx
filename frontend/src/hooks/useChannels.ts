// ============================================
// VAULT TV - Channels Hook (TanStack Query)
// ============================================

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db';
import { playlistManager } from '../services/PlaylistManager';
import type { Channel, ProviderConfig } from '../types';

// Query keys
export const channelKeys = {
  all: ['channels'] as const,
  byProvider: (providerId: string) => [...channelKeys.all, 'provider', providerId] as const,
  byCategory: (providerId: string, category: string) => [...channelKeys.all, 'category', providerId, category] as const,
  favorites: () => [...channelKeys.all, 'favorites'] as const,
  recent: () => [...channelKeys.all, 'recent'] as const,
  search: (query: string) => [...channelKeys.all, 'search', query] as const
};

// Get channels by provider (using Dexie live query for reactivity)
export function useChannelsByProvider(providerId: string | null) {
  return useLiveQuery(
    () => providerId ? db.getChannelsByProvider(providerId) : Promise.resolve([]),
    [providerId],
    []
  );
}

// Get channels by category
export function useChannelsByCategory(providerId: string | null, category: string | null) {
  return useLiveQuery(
    () => providerId && category ? db.getChannelsByCategory(providerId, category) : Promise.resolve([]),
    [providerId, category],
    []
  );
}

// Get favorite channels
export function useFavorites() {
  return useLiveQuery(() => db.getFavorites(), [], []);
}

// Get recently watched
export function useRecentlyWatched(limit = 20) {
  return useLiveQuery(() => db.getRecentlyWatched(limit), [limit], []);
}

// Search channels
export function useChannelSearch(query: string, providerId?: string) {
  return useQuery({
    queryKey: channelKeys.search(query),
    queryFn: () => db.searchChannels(query, providerId),
    enabled: query.length >= 2,
    staleTime: 30000
  });
}

// Toggle favorite mutation
export function useToggleFavorite() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (channelId: string) => db.toggleFavorite(channelId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: channelKeys.favorites() });
    }
  });
}

// Update last watched
export function useUpdateLastWatched() {
  return useMutation({
    mutationFn: (channelId: string) => db.updateLastWatched(channelId)
  });
}

// Add provider mutation
export function useAddProvider() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (config: ProviderConfig) => playlistManager.addProvider(config),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: channelKeys.all });
    }
  });
}

// Sync provider mutation
export function useSyncProvider() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (providerId: string) => playlistManager.syncProvider(providerId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: channelKeys.all });
    }
  });
}

export default useChannelsByProvider;
