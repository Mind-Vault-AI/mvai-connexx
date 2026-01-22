// ============================================
// VAULT TV - VaultPlayer Component
// High-Performance HLS Player with Auto-Retry & Failover
// ============================================

import { useRef, useEffect, useCallback, useState } from 'react';
import {
  MediaPlayer,
  MediaProvider,
  Poster,
  Track,
  useMediaState,
  useMediaRemote,
  type MediaPlayerInstance
} from '@vidstack/react';
import {
  DefaultVideoLayout,
  defaultLayoutIcons
} from '@vidstack/react/player/layouts/default';
import '@vidstack/react/player/styles/default/theme.css';
import '@vidstack/react/player/styles/default/layouts/video.css';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertCircle,
  Loader2,
  SkipForward,
  SkipBack,
  List,
  Settings,
  RefreshCw
} from 'lucide-react';
import { usePlayerStore } from '../../stores/playerStore';
import type { Channel, StreamSource } from '../../types';

interface VaultPlayerProps {
  channel: Channel | null;
  backupSources?: StreamSource[];
  onNextChannel?: () => void;
  onPrevChannel?: () => void;
  onShowEPG?: () => void;
  autoPlay?: boolean;
}

const MAX_RETRIES = 3;
const RETRY_DELAY = 1500;

export function VaultPlayer({
  channel,
  backupSources = [],
  onNextChannel,
  onPrevChannel,
  onShowEPG,
  autoPlay = true
}: VaultPlayerProps) {
  const playerRef = useRef<MediaPlayerInstance>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [currentSourceIndex, setCurrentSourceIndex] = useState(0);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const { setPlaying, setBuffering, setError, clearError } = usePlayerStore();

  // Get all available sources (primary + backups)
  const allSources = channel
    ? [
        { url: channel.streamUrl, priority: 0, type: 'primary' as const, errorCount: 0 },
        ...backupSources
      ]
    : [];

  const currentSource = allSources[currentSourceIndex];

  // Handle stream errors with auto-retry
  const handleError = useCallback((error: Error) => {
    console.error('[VaultPlayer] Stream error:', error.message);

    if (retryCount < MAX_RETRIES) {
      // Retry same source
      setRetryCount(prev => prev + 1);
      setTimeout(() => {
        playerRef.current?.startLoading();
      }, RETRY_DELAY);
    } else if (currentSourceIndex < allSources.length - 1) {
      // Try next backup source
      setRetryCount(0);
      setCurrentSourceIndex(prev => prev + 1);
      console.log('[VaultPlayer] Switching to backup source');
    } else {
      // All sources exhausted
      setShowError(true);
      setErrorMessage('Stream unavailable. Please try another channel.');
      setError({
        code: 'STREAM_FAILED',
        message: error.message,
        retryCount,
        timestamp: Date.now()
      });
    }
  }, [retryCount, currentSourceIndex, allSources.length, setError]);

  // Reset state when channel changes
  useEffect(() => {
    setRetryCount(0);
    setCurrentSourceIndex(0);
    setShowError(false);
    clearError();
  }, [channel?.id, clearError]);

  // Manual retry handler
  const handleManualRetry = () => {
    setRetryCount(0);
    setCurrentSourceIndex(0);
    setShowError(false);
    clearError();
    playerRef.current?.startLoading();
  };

  if (!channel) {
    return (
      <div className="w-full h-full bg-vault-bg flex items-center justify-center">
        <div className="text-vault-text-muted text-lg">
          Select a channel to start watching
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full bg-black">
      <MediaPlayer
        ref={playerRef}
        src={currentSource?.url || ''}
        autoPlay={autoPlay}
        crossOrigin="anonymous"
        playsInline
        onError={(e) => handleError(new Error(String(e)))}
        onPlay={() => setPlaying(true)}
        onPause={() => setPlaying(false)}
        onWaiting={() => setBuffering(true)}
        onPlaying={() => setBuffering(false)}
        className="w-full h-full"
      >
        <MediaProvider>
          {channel.logoUrl && (
            <Poster
              className="vds-poster"
              src={channel.logoUrl}
              alt={channel.name}
            />
          )}
        </MediaProvider>

        <DefaultVideoLayout icons={defaultLayoutIcons} />
      </MediaPlayer>

      {/* Custom Overlay Controls */}
      <PlayerOverlay
        channel={channel}
        retryCount={retryCount}
        onNextChannel={onNextChannel}
        onPrevChannel={onPrevChannel}
        onShowEPG={onShowEPG}
      />

      {/* Error Overlay */}
      <AnimatePresence>
        {showError && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/90 flex flex-col items-center justify-center z-50"
          >
            <AlertCircle className="w-16 h-16 text-vault-primary mb-4" />
            <h3 className="text-xl text-white mb-2">Stream Error</h3>
            <p className="text-vault-text-muted mb-6">{errorMessage}</p>
            <button
              onClick={handleManualRetry}
              className="flex items-center gap-2 px-6 py-3 bg-vault-primary hover:bg-vault-primary-hover rounded-lg transition-colors"
            >
              <RefreshCw className="w-5 h-5" />
              Try Again
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Retry Indicator */}
      <AnimatePresence>
        {retryCount > 0 && !showError && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="absolute bottom-20 left-1/2 -translate-x-1/2 bg-black/80 px-4 py-2 rounded-full flex items-center gap-2"
          >
            <Loader2 className="w-4 h-4 animate-spin text-vault-primary" />
            <span className="text-sm text-white">
              Reconnecting... ({retryCount}/{MAX_RETRIES})
            </span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Player Overlay with Custom Controls
function PlayerOverlay({
  channel,
  retryCount,
  onNextChannel,
  onPrevChannel,
  onShowEPG
}: {
  channel: Channel;
  retryCount: number;
  onNextChannel?: () => void;
  onPrevChannel?: () => void;
  onShowEPG?: () => void;
}) {
  const [showOverlay, setShowOverlay] = useState(false);
  const hideTimeout = useRef<ReturnType<typeof setTimeout>>();

  const handleMouseMove = () => {
    setShowOverlay(true);
    clearTimeout(hideTimeout.current);
    hideTimeout.current = setTimeout(() => setShowOverlay(false), 3000);
  };

  useEffect(() => {
    return () => clearTimeout(hideTimeout.current);
  }, []);

  return (
    <div
      className="absolute inset-0 z-40"
      onMouseMove={handleMouseMove}
      onMouseLeave={() => setShowOverlay(false)}
    >
      <AnimatePresence>
        {showOverlay && (
          <>
            {/* Top Bar - Channel Info */}
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/80 to-transparent"
            >
              <div className="flex items-center gap-3">
                {channel.logoUrl && (
                  <img
                    src={channel.logoUrl}
                    alt=""
                    className="w-10 h-10 rounded object-contain bg-white/10"
                  />
                )}
                <div>
                  <h2 className="text-white font-semibold">{channel.name}</h2>
                  <p className="text-vault-text-muted text-sm">{channel.groupTitle}</p>
                </div>
              </div>
            </motion.div>

            {/* Side Controls */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="absolute right-4 top-1/2 -translate-y-1/2 flex flex-col gap-2"
            >
              {onPrevChannel && (
                <OverlayButton onClick={onPrevChannel} title="Previous Channel">
                  <SkipBack className="w-5 h-5" />
                </OverlayButton>
              )}
              {onNextChannel && (
                <OverlayButton onClick={onNextChannel} title="Next Channel">
                  <SkipForward className="w-5 h-5" />
                </OverlayButton>
              )}
              {onShowEPG && (
                <OverlayButton onClick={onShowEPG} title="Show EPG">
                  <List className="w-5 h-5" />
                </OverlayButton>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}

function OverlayButton({
  children,
  onClick,
  title
}: {
  children: React.ReactNode;
  onClick: () => void;
  title: string;
}) {
  return (
    <button
      onClick={onClick}
      title={title}
      className="p-3 bg-black/60 hover:bg-black/80 rounded-full text-white transition-colors"
    >
      {children}
    </button>
  );
}

export default VaultPlayer;
