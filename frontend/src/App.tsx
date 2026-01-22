// ============================================
// VAULT TV - Main App Component
// ============================================

import { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MainLayout } from './components/Layout/MainLayout';
import { LiveTV } from './views/LiveTV';
import { Settings } from './views/Settings';
import { useAppStore } from './stores/appStore';
import { db } from './db';

// Create Query Client with optimized defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30, // 30 minutes (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: false
    }
  }
});

function AppContent() {
  const { currentView, setInitialized, isInitialized } = useAppStore();

  // Initialize app
  useEffect(() => {
    const init = async () => {
      try {
        // Ensure database is ready
        await db.open();

        // Load preferences
        const prefs = await db.getPreferences();
        if (!prefs) {
          await db.savePreferences({});
        }

        setInitialized(true);
        console.log('[VaultTV] App initialized');
      } catch (error) {
        console.error('[VaultTV] Initialization error:', error);
        setInitialized(true); // Continue anyway
      }
    };

    init();
  }, [setInitialized]);

  // Show loading state
  if (!isInitialized) {
    return (
      <div className="h-screen w-screen bg-vault-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-vault-primary rounded-2xl flex items-center justify-center mx-auto mb-4 animate-pulse">
            <svg className="w-10 h-10 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <p className="text-vault-text-muted">Loading Vault TV...</p>
        </div>
      </div>
    );
  }

  // Render current view
  const renderView = () => {
    switch (currentView) {
      case 'live':
        return <LiveTV />;
      case 'movies':
        return <MoviesPlaceholder />;
      case 'series':
        return <SeriesPlaceholder />;
      case 'favorites':
        return <FavoritesPlaceholder />;
      case 'recordings':
        return <RecordingsPlaceholder />;
      case 'settings':
        return <Settings />;
      default:
        return <LiveTV />;
    }
  };

  return <MainLayout>{renderView()}</MainLayout>;
}

// Placeholder components for views not yet implemented
function MoviesPlaceholder() {
  return (
    <div className="h-full flex items-center justify-center text-vault-text-muted">
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Movies</h2>
        <p>VOD content coming soon</p>
      </div>
    </div>
  );
}

function SeriesPlaceholder() {
  return (
    <div className="h-full flex items-center justify-center text-vault-text-muted">
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Series</h2>
        <p>TV Series content coming soon</p>
      </div>
    </div>
  );
}

function FavoritesPlaceholder() {
  return (
    <div className="h-full flex items-center justify-center text-vault-text-muted">
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Favorites</h2>
        <p>Your favorite channels will appear here</p>
      </div>
    </div>
  );
}

function RecordingsPlaceholder() {
  return (
    <div className="h-full flex items-center justify-center text-vault-text-muted">
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Recordings</h2>
        <p>Cloud DVR - Premium feature</p>
      </div>
    </div>
  );
}

// Main App with providers
export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
