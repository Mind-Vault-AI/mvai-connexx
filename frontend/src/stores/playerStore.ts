// ============================================
// VAULT TV - Player Store (Zustand)
// Fast, ephemeral state for playback
// ============================================

import { create } from 'zustand';
import type { PlaybackState, PlaybackError, StreamQuality, Channel } from '../types';

interface PlayerStore extends PlaybackState {
  // Current channel
  currentChannel: Channel | null;

  // Actions
  setChannel: (channel: Channel | null) => void;
  setPlaying: (isPlaying: boolean) => void;
  setBuffering: (isBuffering: boolean) => void;
  setVolume: (volume: number) => void;
  setMuted: (isMuted: boolean) => void;
  setQuality: (quality: StreamQuality) => void;
  setError: (error: PlaybackError) => void;
  clearError: () => void;
  setCurrentTime: (time: number) => void;
  setDuration: (duration: number) => void;
  reset: () => void;
}

const initialState: Omit<PlayerStore, 'setChannel' | 'setPlaying' | 'setBuffering' | 'setVolume' | 'setMuted' | 'setQuality' | 'setError' | 'clearError' | 'setCurrentTime' | 'setDuration' | 'reset'> = {
  currentChannel: null,
  channelId: null,
  isPlaying: false,
  isBuffering: false,
  currentTime: 0,
  duration: 0,
  volume: 1,
  isMuted: false,
  quality: { label: 'Auto', bitrate: 0, isAuto: true },
  error: null
};

export const usePlayerStore = create<PlayerStore>((set) => ({
  ...initialState,

  setChannel: (channel) =>
    set({
      currentChannel: channel,
      channelId: channel?.id || null,
      error: null,
      isBuffering: false
    }),

  setPlaying: (isPlaying) => set({ isPlaying }),

  setBuffering: (isBuffering) => set({ isBuffering }),

  setVolume: (volume) => set({ volume, isMuted: volume === 0 }),

  setMuted: (isMuted) => set({ isMuted }),

  setQuality: (quality) => set({ quality }),

  setError: (error) => set({ error, isPlaying: false }),

  clearError: () => set({ error: null }),

  setCurrentTime: (currentTime) => set({ currentTime }),

  setDuration: (duration) => set({ duration }),

  reset: () => set(initialState)
}));

export default usePlayerStore;
