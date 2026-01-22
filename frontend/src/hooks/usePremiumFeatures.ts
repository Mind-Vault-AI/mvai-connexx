// ============================================
// VAULT TV - Premium Features Hook
// Revenue Foundation: Feature Gating
// ============================================

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { PremiumStatus, PremiumFeature } from '../types';

interface PremiumStore extends PremiumStatus {
  // Actions
  setPremiumStatus: (status: Partial<PremiumStatus>) => void;
  checkFeature: (feature: PremiumFeature) => boolean;
  upgrade: (plan: 'premium' | 'ultimate') => void;
  reset: () => void;
}

// Feature definitions per plan
const PLAN_FEATURES: Record<string, PremiumFeature[]> = {
  free: [],
  premium: ['multi_view', 'cloud_dvr', 'no_buffer', 'unlimited_playlists', 'catch_up'],
  ultimate: ['multi_view', 'cloud_dvr', 'no_buffer', '4k_upscale', 'ai_search', 'unlimited_playlists', 'catch_up', 'timeshift']
};

// Free tier limits
const FREE_LIMITS = {
  maxPlaylists: 1,
  maxFavorites: 50,
  maxRecordings: 0,
  streamQuality: '720p'
} as const;

const usePremiumStore = create<PremiumStore>()(
  persist(
    (set, get) => ({
      isPremium: false,
      plan: 'free',
      expiresAt: undefined,
      features: [],

      setPremiumStatus: (status) =>
        set((state) => ({
          ...state,
          ...status,
          features: PLAN_FEATURES[status.plan || state.plan] || []
        })),

      checkFeature: (feature) => {
        const state = get();
        if (state.plan === 'free') return false;
        if (state.expiresAt && state.expiresAt < Date.now()) return false;
        return state.features.includes(feature);
      },

      upgrade: (plan) =>
        set({
          isPremium: true,
          plan,
          features: PLAN_FEATURES[plan],
          expiresAt: Date.now() + 30 * 24 * 60 * 60 * 1000 // 30 days
        }),

      reset: () =>
        set({
          isPremium: false,
          plan: 'free',
          features: [],
          expiresAt: undefined
        })
    }),
    {
      name: 'vault-tv-premium'
    }
  )
);

// Main hook
export function usePremiumFeatures() {
  const store = usePremiumStore();

  return {
    isPremium: store.isPremium,
    plan: store.plan,
    features: store.features,
    expiresAt: store.expiresAt,

    // Feature checks
    hasFeature: store.checkFeature,
    canUseMultiView: () => store.checkFeature('multi_view'),
    canUseCloudDVR: () => store.checkFeature('cloud_dvr'),
    canUse4K: () => store.checkFeature('4k_upscale'),
    canUseAISearch: () => store.checkFeature('ai_search'),
    canUseCatchUp: () => store.checkFeature('catch_up'),
    canUseTimeshift: () => store.checkFeature('timeshift'),

    // Limits for free tier
    limits: store.plan === 'free' ? FREE_LIMITS : null,

    // Actions
    upgrade: store.upgrade,
    setPremiumStatus: store.setPremiumStatus
  };
}

// Premium gate component helper
export function usePremiumGate(feature: PremiumFeature) {
  const { hasFeature, plan } = usePremiumFeatures();
  const isAllowed = hasFeature(feature);

  return {
    isAllowed,
    isPremiumRequired: !isAllowed && plan === 'free',
    showUpgradePrompt: !isAllowed
  };
}

export default usePremiumFeatures;
