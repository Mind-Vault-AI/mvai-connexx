// ============================================
// VAULT TV - PlaylistManager Service
// Universal Adapter: Xtream, M3U, Stremio -> Standard Format
// ============================================

import { db } from '../db';
import type {
  Provider,
  ProviderConfig,
  XtreamCredentials,
  M3USource,
  Channel,
  Category,
  XtreamAuthResponse,
  XtreamCategory,
  XtreamChannel,
  M3UEntry
} from '../types';

// Web Worker for parsing (non-blocking UI)
const createParserWorker = () => {
  const workerCode = `
    self.onmessage = async (e) => {
      const { type, payload, requestId } = e.data;

      try {
        let result;

        if (type === 'PARSE_M3U') {
          result = parseM3U(payload.content, payload.providerId);
        } else if (type === 'PARSE_XTREAM_CHANNELS') {
          result = parseXtreamChannels(payload.channels, payload.providerId, payload.baseUrl);
        }

        self.postMessage({ type: type + '_RESULT', payload: result, requestId });
      } catch (error) {
        self.postMessage({ type: 'ERROR', error: error.message, requestId });
      }
    };

    function parseM3U(content, providerId) {
      const lines = content.split('\\n');
      const channels = [];
      let currentEntry = null;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();

        if (line.startsWith('#EXTINF:')) {
          const duration = parseInt(line.match(/#EXTINF:(-?\\d+)/)?.[1] || '-1');
          const tvgId = line.match(/tvg-id="([^"]*)"/)?.[1] || '';
          const tvgName = line.match(/tvg-name="([^"]*)"/)?.[1] || '';
          const tvgLogo = line.match(/tvg-logo="([^"]*)"/)?.[1] || '';
          const groupTitle = line.match(/group-title="([^"]*)"/)?.[1] || 'Uncategorized';
          const title = line.split(',').pop()?.trim() || 'Unknown';

          currentEntry = { duration, tvgId, tvgName, tvgLogo, groupTitle, title };
        } else if (line && !line.startsWith('#') && currentEntry) {
          channels.push({
            id: providerId + '_' + channels.length,
            providerId,
            name: currentEntry.tvgName || currentEntry.title,
            logoUrl: currentEntry.tvgLogo || undefined,
            groupTitle: currentEntry.groupTitle,
            streamUrl: line,
            streamType: detectStreamType(line, currentEntry.groupTitle),
            epgId: currentEntry.tvgId || undefined,
            isFavorite: false,
            addedAt: Date.now()
          });
          currentEntry = null;
        }
      }

      return channels;
    }

    function parseXtreamChannels(channels, providerId, baseUrl) {
      return channels.map((ch, index) => ({
        id: providerId + '_' + ch.stream_id,
        providerId,
        name: ch.name,
        logoUrl: ch.stream_icon || undefined,
        groupTitle: ch.category_id || 'Uncategorized',
        streamUrl: baseUrl + '/' + ch.stream_id + '.m3u8',
        streamType: ch.stream_type === 'live' ? 'live' : ch.stream_type === 'movie' ? 'movie' : 'series',
        epgId: ch.epg_channel_id || undefined,
        number: ch.num,
        isFavorite: false,
        addedAt: Date.now()
      }));
    }

    function detectStreamType(url, groupTitle) {
      const lower = (url + groupTitle).toLowerCase();
      if (lower.includes('movie') || lower.includes('film') || lower.includes('vod')) return 'movie';
      if (lower.includes('series') || lower.includes('episode')) return 'series';
      return 'live';
    }
  `;

  const blob = new Blob([workerCode], { type: 'application/javascript' });
  return new Worker(URL.createObjectURL(blob));
};

class PlaylistManager {
  private worker: Worker | null = null;
  private requestId = 0;
  private pendingRequests = new Map<string, { resolve: (value: unknown) => void; reject: (error: Error) => void }>();

  constructor() {
    this.initWorker();
  }

  private initWorker(): void {
    if (typeof Worker !== 'undefined') {
      this.worker = createParserWorker();
      this.worker.onmessage = (e) => {
        const { requestId, payload, error } = e.data;
        const pending = this.pendingRequests.get(requestId);
        if (pending) {
          if (error) {
            pending.reject(new Error(error));
          } else {
            pending.resolve(payload);
          }
          this.pendingRequests.delete(requestId);
        }
      };
    }
  }

  private sendToWorker<T>(type: string, payload: unknown): Promise<T> {
    return new Promise((resolve, reject) => {
      if (!this.worker) {
        reject(new Error('Web Worker not available'));
        return;
      }
      const requestId = String(++this.requestId);
      this.pendingRequests.set(requestId, { resolve: resolve as (value: unknown) => void, reject });
      this.worker.postMessage({ type, payload, requestId });
    });
  }

  // ========== PROVIDER MANAGEMENT ==========

  async addProvider(config: ProviderConfig): Promise<Provider> {
    const id = crypto.randomUUID();
    const provider: Provider = {
      id,
      config,
      name: config.name || this.getProviderName(config),
      status: 'syncing',
      channelCount: 0,
      createdAt: Date.now()
    };

    await db.providers.add(provider);

    // Start sync in background
    this.syncProvider(id).catch(console.error);

    return provider;
  }

  async removeProvider(providerId: string): Promise<void> {
    await db.clearProviderData(providerId);
    await db.providers.delete(providerId);
  }

  async syncProvider(providerId: string): Promise<void> {
    const provider = await db.providers.get(providerId);
    if (!provider) throw new Error('Provider not found');

    await db.updateProviderStatus(providerId, 'syncing');

    try {
      const { channels, categories } = await this.fetchProviderData(provider.config, providerId);

      await db.clearProviderData(providerId);
      await db.bulkUpsertChannels(channels);
      await db.bulkUpsertCategories(categories);
      await db.updateProviderStatus(providerId, 'active', channels.length);

      console.log(`[PlaylistManager] Synced ${channels.length} channels for provider ${providerId}`);
    } catch (error) {
      console.error('[PlaylistManager] Sync failed:', error);
      await db.updateProviderStatus(providerId, 'error');
      throw error;
    }
  }

  // ========== DATA FETCHING ==========

  private async fetchProviderData(
    config: ProviderConfig,
    providerId: string
  ): Promise<{ channels: Channel[]; categories: Category[] }> {
    switch (config.type) {
      case 'xtream':
        return this.fetchXtreamData(config, providerId);
      case 'm3u':
        return this.fetchM3UData(config, providerId);
      case 'stremio':
        return this.fetchStremioData(config, providerId);
      default:
        throw new Error('Unknown provider type');
    }
  }

  private async fetchXtreamData(
    config: XtreamCredentials,
    providerId: string
  ): Promise<{ channels: Channel[]; categories: Category[] }> {
    const baseUrl = config.serverUrl.replace(/\/$/, '');
    const authUrl = `${baseUrl}/player_api.php?username=${encodeURIComponent(config.username)}&password=${encodeURIComponent(config.password)}`;

    // Authenticate
    const authResponse = await fetch(authUrl);
    if (!authResponse.ok) throw new Error('Authentication failed');

    const authData: XtreamAuthResponse = await authResponse.json();
    if (authData.user_info.auth !== 1) throw new Error('Invalid credentials');

    // Fetch categories and channels in parallel
    const [liveCategories, vodCategories, liveCh, vodCh] = await Promise.all([
      fetch(`${authUrl}&action=get_live_categories`).then(r => r.json()) as Promise<XtreamCategory[]>,
      fetch(`${authUrl}&action=get_vod_categories`).then(r => r.json()) as Promise<XtreamCategory[]>,
      fetch(`${authUrl}&action=get_live_streams`).then(r => r.json()) as Promise<XtreamChannel[]>,
      fetch(`${authUrl}&action=get_vod_streams`).then(r => r.json()) as Promise<XtreamChannel[]>
    ]);

    // Build stream base URL
    const protocol = authData.server_info.server_protocol || 'http';
    const port = authData.server_info.port;
    const streamBase = `${protocol}://${new URL(baseUrl).hostname}:${port}/${config.username}/${config.password}`;

    // Parse channels using Web Worker
    const liveChannels = await this.sendToWorker<Channel[]>('PARSE_XTREAM_CHANNELS', {
      channels: liveCh,
      providerId,
      baseUrl: streamBase
    });

    const vodChannels: Channel[] = vodCh.map((ch, index) => ({
      id: `${providerId}_vod_${ch.stream_id}`,
      providerId,
      name: ch.name,
      logoUrl: ch.stream_icon || undefined,
      groupTitle: ch.category_id || 'Movies',
      streamUrl: `${streamBase}/movie/${ch.stream_id}.mp4`,
      streamType: 'movie' as const,
      isFavorite: false,
      addedAt: Date.now()
    }));

    // Build categories
    const categories: Category[] = [
      ...liveCategories.map(cat => ({
        id: `${providerId}_live_${cat.category_id}`,
        providerId,
        name: cat.category_name,
        type: 'live' as const,
        channelCount: liveCh.filter(ch => ch.category_id === cat.category_id).length
      })),
      ...vodCategories.map(cat => ({
        id: `${providerId}_vod_${cat.category_id}`,
        providerId,
        name: cat.category_name,
        type: 'movie' as const,
        channelCount: vodCh.filter(ch => ch.category_id === cat.category_id).length
      }))
    ];

    return {
      channels: [...liveChannels, ...vodChannels],
      categories
    };
  }

  private async fetchM3UData(
    config: M3USource,
    providerId: string
  ): Promise<{ channels: Channel[]; categories: Category[] }> {
    const response = await fetch(config.url);
    if (!response.ok) throw new Error('Failed to fetch M3U');

    const content = await response.text();

    // Parse using Web Worker
    const channels = await this.sendToWorker<Channel[]>('PARSE_M3U', {
      content,
      providerId
    });

    // Extract unique categories
    const categoryMap = new Map<string, number>();
    channels.forEach(ch => {
      const count = categoryMap.get(ch.groupTitle) || 0;
      categoryMap.set(ch.groupTitle, count + 1);
    });

    const categories: Category[] = Array.from(categoryMap.entries()).map(([name, count]) => ({
      id: `${providerId}_cat_${name.replace(/\s+/g, '_')}`,
      providerId,
      name,
      type: 'live' as const,
      channelCount: count
    }));

    return { channels, categories };
  }

  private async fetchStremioData(
    config: { type: 'stremio'; manifestUrl: string; name?: string },
    providerId: string
  ): Promise<{ channels: Channel[]; categories: Category[] }> {
    // Fetch Stremio addon manifest
    const response = await fetch(config.manifestUrl);
    if (!response.ok) throw new Error('Failed to fetch Stremio manifest');

    const manifest = await response.json();

    // For now, return empty - Stremio integration requires more complex catalog handling
    console.log('[PlaylistManager] Stremio addon loaded:', manifest.name);

    return { channels: [], categories: [] };
  }

  // ========== HELPERS ==========

  private getProviderName(config: ProviderConfig): string {
    switch (config.type) {
      case 'xtream':
        return new URL(config.serverUrl).hostname;
      case 'm3u':
        return 'M3U Playlist';
      case 'stremio':
        return 'Stremio Addon';
    }
  }

  // ========== DELTA SYNC ==========

  async deltaSyncProvider(providerId: string): Promise<{ added: number; removed: number; updated: number }> {
    const provider = await db.providers.get(providerId);
    if (!provider) throw new Error('Provider not found');

    const existingChannels = await db.getChannelsByProvider(providerId);
    const existingIds = new Set(existingChannels.map(c => c.id));

    const { channels: newChannels } = await this.fetchProviderData(provider.config, providerId);
    const newIds = new Set(newChannels.map(c => c.id));

    let added = 0, removed = 0, updated = 0;

    // Find channels to add
    const toAdd = newChannels.filter(c => !existingIds.has(c.id));
    added = toAdd.length;

    // Find channels to remove
    const toRemove = existingChannels.filter(c => !newIds.has(c.id));
    removed = toRemove.length;

    // Apply changes
    if (toAdd.length > 0) {
      await db.bulkUpsertChannels(toAdd);
    }

    if (toRemove.length > 0) {
      await Promise.all(toRemove.map(c => db.channels.delete(c.id)));
    }

    await db.updateProviderStatus(providerId, 'active', newChannels.length);

    return { added, removed, updated };
  }

  destroy(): void {
    this.worker?.terminate();
    this.worker = null;
  }
}

export const playlistManager = new PlaylistManager();
export default playlistManager;
