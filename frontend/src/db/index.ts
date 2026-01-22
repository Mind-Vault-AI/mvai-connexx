// ============================================
// VAULT TV - Dexie.js Database Layer
// Local-First Architecture for 99.9% Uptime
// ============================================

import Dexie, { Table } from 'dexie';
import type {
  Channel,
  Category,
  Provider,
  EPGProgram,
  Recording,
  UserPreferences
} from '../types';

class VaultDatabase extends Dexie {
  channels!: Table<Channel>;
  categories!: Table<Category>;
  providers!: Table<Provider>;
  epgPrograms!: Table<EPGProgram>;
  recordings!: Table<Recording>;
  preferences!: Table<UserPreferences & { id: string }>;
  cache!: Table<{ key: string; value: unknown; expiresAt: number }>;

  constructor() {
    super('VaultTV');

    this.version(1).stores({
      channels: 'id, providerId, name, groupTitle, streamType, [providerId+groupTitle], [providerId+streamType], lastWatched, isFavorite',
      categories: 'id, providerId, name, type, [providerId+type]',
      providers: 'id, status, lastSync',
      epgPrograms: 'id, channelId, start, end, [channelId+start]',
      recordings: 'id, channelId, status, startTime',
      preferences: 'id',
      cache: 'key, expiresAt'
    });
  }

  // ========== CHANNEL OPERATIONS ==========

  async getChannelsByProvider(providerId: string): Promise<Channel[]> {
    return this.channels.where('providerId').equals(providerId).toArray();
  }

  async getChannelsByCategory(providerId: string, groupTitle: string): Promise<Channel[]> {
    return this.channels
      .where('[providerId+groupTitle]')
      .equals([providerId, groupTitle])
      .toArray();
  }

  async getChannelsByType(providerId: string, streamType: 'live' | 'movie' | 'series'): Promise<Channel[]> {
    return this.channels
      .where('[providerId+streamType]')
      .equals([providerId, streamType])
      .toArray();
  }

  async getFavorites(): Promise<Channel[]> {
    return this.channels.filter(c => c.isFavorite).toArray();
  }

  async getRecentlyWatched(limit = 20): Promise<Channel[]> {
    return this.channels
      .orderBy('lastWatched')
      .reverse()
      .filter(c => c.lastWatched !== undefined)
      .limit(limit)
      .toArray();
  }

  async updateLastWatched(channelId: string): Promise<void> {
    await this.channels.update(channelId, { lastWatched: Date.now() });
  }

  async toggleFavorite(channelId: string): Promise<boolean> {
    const channel = await this.channels.get(channelId);
    if (!channel) return false;
    const newValue = !channel.isFavorite;
    await this.channels.update(channelId, { isFavorite: newValue });
    return newValue;
  }

  async searchChannels(query: string, providerId?: string): Promise<Channel[]> {
    const lowerQuery = query.toLowerCase();
    let collection = this.channels.toCollection();
    if (providerId) {
      collection = this.channels.where('providerId').equals(providerId);
    }
    return collection
      .filter(channel =>
        channel.name.toLowerCase().includes(lowerQuery) ||
        channel.groupTitle.toLowerCase().includes(lowerQuery)
      )
      .limit(100)
      .toArray();
  }

  // ========== BULK OPERATIONS ==========

  async bulkUpsertChannels(channels: Channel[]): Promise<void> {
    await this.channels.bulkPut(channels);
  }

  async bulkUpsertCategories(categories: Category[]): Promise<void> {
    await this.categories.bulkPut(categories);
  }

  async bulkUpsertEPG(programs: EPGProgram[]): Promise<void> {
    await this.epgPrograms.bulkPut(programs);
  }

  async clearProviderData(providerId: string): Promise<void> {
    await this.transaction('rw', [this.channels, this.categories, this.epgPrograms], async () => {
      await this.channels.where('providerId').equals(providerId).delete();
      await this.categories.where('providerId').equals(providerId).delete();
    });
  }

  // ========== EPG OPERATIONS ==========

  async getCurrentProgram(channelId: string): Promise<EPGProgram | undefined> {
    const now = Date.now();
    return this.epgPrograms
      .where('[channelId+start]')
      .between([channelId, 0], [channelId, now])
      .filter(p => p.end > now)
      .first();
  }

  async getUpcomingPrograms(channelId: string, hours = 24): Promise<EPGProgram[]> {
    const now = Date.now();
    const endTime = now + (hours * 60 * 60 * 1000);
    return this.epgPrograms
      .where('channelId')
      .equals(channelId)
      .filter(p => p.start >= now && p.start <= endTime)
      .sortBy('start');
  }

  async cleanExpiredEPG(): Promise<number> {
    const yesterday = Date.now() - (24 * 60 * 60 * 1000);
    return this.epgPrograms.where('end').below(yesterday).delete();
  }

  // ========== PROVIDER OPERATIONS ==========

  async getActiveProviders(): Promise<Provider[]> {
    return this.providers.where('status').equals('active').toArray();
  }

  async updateProviderStatus(
    providerId: string,
    status: Provider['status'],
    channelCount?: number
  ): Promise<void> {
    const updates: Partial<Provider> = { status, lastSync: Date.now() };
    if (channelCount !== undefined) {
      updates.channelCount = channelCount;
    }
    await this.providers.update(providerId, updates);
  }

  // ========== CACHE OPERATIONS ==========

  async getCached<T>(key: string): Promise<T | null> {
    const cached = await this.cache.get(key);
    if (!cached) return null;
    if (cached.expiresAt < Date.now()) {
      await this.cache.delete(key);
      return null;
    }
    return cached.value as T;
  }

  async setCache(key: string, value: unknown, ttlMs: number): Promise<void> {
    await this.cache.put({ key, value, expiresAt: Date.now() + ttlMs });
  }

  async clearExpiredCache(): Promise<void> {
    await this.cache.where('expiresAt').below(Date.now()).delete();
  }

  // ========== PREFERENCES ==========

  async getPreferences(): Promise<UserPreferences | null> {
    const prefs = await this.preferences.get('default');
    if (!prefs) return null;
    const { id: _, ...preferences } = prefs;
    return preferences;
  }

  async savePreferences(preferences: Partial<UserPreferences>): Promise<void> {
    const existing = await this.preferences.get('default');
    await this.preferences.put({
      id: 'default',
      ...this.getDefaultPreferences(),
      ...existing,
      ...preferences
    });
  }

  private getDefaultPreferences(): UserPreferences {
    return {
      theme: 'dark',
      defaultQuality: 'auto',
      autoPlay: true,
      bufferSize: 'medium',
      showAdultContent: false,
      language: 'en',
      epgTimeOffset: 0,
      vpnEnabled: false
    };
  }

  // ========== STATISTICS ==========

  async getStats(): Promise<{
    totalChannels: number;
    totalProviders: number;
    totalFavorites: number;
    epgProgramsCount: number;
  }> {
    const [totalChannels, totalProviders, totalFavorites, epgProgramsCount] = await Promise.all([
      this.channels.count(),
      this.providers.count(),
      this.channels.filter(c => c.isFavorite).count(),
      this.epgPrograms.count()
    ]);
    return { totalChannels, totalProviders, totalFavorites, epgProgramsCount };
  }
}

export const db = new VaultDatabase();

db.on('ready', async () => {
  await Promise.all([db.cleanExpiredEPG(), db.clearExpiredCache()]);
  console.log('[VaultDB] Database ready');
});

export default db;
