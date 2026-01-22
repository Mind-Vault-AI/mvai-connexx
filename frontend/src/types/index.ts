// ============================================
// VAULT TV - Core Type Definitions
// ============================================

// Provider Types
export type ProviderType = 'xtream' | 'm3u' | 'stremio';

export interface XtreamCredentials {
  type: 'xtream';
  serverUrl: string;
  username: string;
  password: string;
  name?: string;
}

export interface M3USource {
  type: 'm3u';
  url: string;
  name?: string;
  epgUrl?: string;
}

export interface StremioAddon {
  type: 'stremio';
  manifestUrl: string;
  name?: string;
}

export type ProviderConfig = XtreamCredentials | M3USource | StremioAddon;

// Channel & Content Types
export interface Channel {
  id: string;
  providerId: string;
  name: string;
  logoUrl?: string;
  groupTitle: string;
  streamUrl: string;
  streamType: 'live' | 'movie' | 'series';
  epgId?: string;
  number?: number;
  isFavorite: boolean;
  lastWatched?: number;
  addedAt: number;
}

export interface Category {
  id: string;
  providerId: string;
  name: string;
  type: 'live' | 'movie' | 'series';
  parentId?: string;
  channelCount: number;
}

// EPG Types
export interface EPGProgram {
  id: string;
  channelId: string;
  title: string;
  description?: string;
  start: number;
  end: number;
  category?: string;
  posterUrl?: string;
  rating?: string;
}

export interface EPGChannel {
  id: string;
  name: string;
  logoUrl?: string;
  programs: EPGProgram[];
}

// Provider Status
export interface Provider {
  id: string;
  config: ProviderConfig;
  name: string;
  status: 'active' | 'error' | 'syncing' | 'offline';
  lastSync?: number;
  channelCount: number;
  expiresAt?: number;
  maxConnections?: number;
  activeConnections?: number;
  createdAt: number;
}

// Playback Types
export interface PlaybackState {
  channelId: string | null;
  isPlaying: boolean;
  isBuffering: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  isMuted: boolean;
  quality: StreamQuality;
  error: PlaybackError | null;
}

export interface StreamQuality {
  label: string;
  bitrate: number;
  resolution?: string;
  isAuto: boolean;
}

export interface PlaybackError {
  code: string;
  message: string;
  retryCount: number;
  timestamp: number;
}

// Stream Source for Failover
export interface StreamSource {
  url: string;
  priority: number;
  type: 'primary' | 'backup' | 'cdn';
  lastError?: number;
  errorCount: number;
}

// User Preferences
export interface UserPreferences {
  theme: 'dark' | 'light' | 'system';
  defaultQuality: 'auto' | '4k' | '1080p' | '720p' | '480p';
  autoPlay: boolean;
  bufferSize: 'low' | 'medium' | 'high';
  showAdultContent: boolean;
  language: string;
  epgTimeOffset: number;
  realDebridToken?: string;
  vpnEnabled: boolean;
}

// Premium Features
export interface PremiumStatus {
  isPremium: boolean;
  plan: 'free' | 'premium' | 'ultimate';
  expiresAt?: number;
  features: PremiumFeature[];
}

export type PremiumFeature =
  | 'multi_view'
  | 'cloud_dvr'
  | 'no_buffer'
  | '4k_upscale'
  | 'ai_search'
  | 'unlimited_playlists'
  | 'catch_up'
  | 'timeshift';

// Recording Types
export interface Recording {
  id: string;
  channelId: string;
  channelName: string;
  programTitle: string;
  startTime: number;
  endTime: number;
  status: 'scheduled' | 'recording' | 'completed' | 'failed';
  filePath?: string;
  fileSize?: number;
  cloudProvider?: 'gdrive' | 'webdav' | 'dropbox';
}

// Search Types
export interface SearchResult {
  id: string;
  type: 'channel' | 'movie' | 'series' | 'program';
  title: string;
  subtitle?: string;
  imageUrl?: string;
  providerId: string;
  relevanceScore: number;
}

// Sync Types
export interface SyncStatus {
  providerId: string;
  status: 'idle' | 'syncing' | 'error' | 'complete';
  progress: number;
  totalChannels: number;
  syncedChannels: number;
  lastSync?: number;
  error?: string;
}

// App State Types
export interface AppState {
  isOnline: boolean;
  isInitialized: boolean;
  activeProviderId: string | null;
  sidebarCollapsed: boolean;
  currentView: ViewType;
}

export type ViewType = 'live' | 'movies' | 'series' | 'favorites' | 'recordings' | 'settings' | 'search';

// Worker Message Types
export interface WorkerMessage<T = unknown> {
  type: string;
  payload: T;
  requestId: string;
}

export interface WorkerResponse<T = unknown> {
  type: string;
  payload: T;
  requestId: string;
  error?: string;
}

// Xtream API Types
export interface XtreamAuthResponse {
  user_info: {
    username: string;
    password: string;
    message: string;
    auth: number;
    status: string;
    exp_date: string;
    is_trial: string;
    active_cons: string;
    created_at: string;
    max_connections: string;
    allowed_output_formats: string[];
  };
  server_info: {
    url: string;
    port: string;
    https_port: string;
    server_protocol: string;
    rtmp_port: string;
    timezone: string;
    timestamp_now: number;
    time_now: string;
  };
}

export interface XtreamCategory {
  category_id: string;
  category_name: string;
  parent_id: number;
}

export interface XtreamChannel {
  num: number;
  name: string;
  stream_type: string;
  stream_id: number;
  stream_icon: string;
  epg_channel_id: string;
  added: string;
  category_id: string;
  custom_sid: string;
  tv_archive: number;
  direct_source: string;
  tv_archive_duration: number;
}

// M3U Types
export interface M3UEntry {
  duration: number;
  title: string;
  tvgId?: string;
  tvgName?: string;
  tvgLogo?: string;
  groupTitle?: string;
  url: string;
}
