// ============================================
// VAULT TV - App Store (Zustand)
// Global application state
// ============================================

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AppState, ViewType } from '../types';

interface AppStore extends AppState {
  // Actions
  setOnline: (isOnline: boolean) => void;
  setInitialized: (isInitialized: boolean) => void;
  setActiveProvider: (providerId: string | null) => void;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setCurrentView: (view: ViewType) => void;
}

export const useAppStore = create<AppStore>()(
  persist(
    (set) => ({
      isOnline: navigator.onLine,
      isInitialized: false,
      activeProviderId: null,
      sidebarCollapsed: false,
      currentView: 'live',

      setOnline: (isOnline) => set({ isOnline }),

      setInitialized: (isInitialized) => set({ isInitialized }),

      setActiveProvider: (activeProviderId) => set({ activeProviderId }),

      toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

      setSidebarCollapsed: (sidebarCollapsed) => set({ sidebarCollapsed }),

      setCurrentView: (currentView) => set({ currentView })
    }),
    {
      name: 'vault-tv-app',
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
        activeProviderId: state.activeProviderId
      })
    }
  )
);

// Listen to online/offline events
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => useAppStore.getState().setOnline(true));
  window.addEventListener('offline', () => useAppStore.getState().setOnline(false));
}

export default useAppStore;
