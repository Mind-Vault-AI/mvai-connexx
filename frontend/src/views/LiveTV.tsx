// ============================================
// VAULT TV - Live TV View
// ============================================

import { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { VaultPlayer } from '../components/Player/VaultPlayer';
import { ChannelGrid } from '../components/ChannelList/ChannelGrid';
import { useAppStore } from '../stores/appStore';
import { usePlayerStore } from '../stores/playerStore';
import { useChannelsByProvider, useToggleFavorite, useUpdateLastWatched } from '../hooks/useChannels';
import type { Channel } from '../types';

export function LiveTV() {
  const { activeProviderId } = useAppStore();
  const { currentChannel, setChannel } = usePlayerStore();
  const [showChannelList, setShowChannelList] = useState(true);

  const channels = useChannelsByProvider(activeProviderId);
  const liveChannels = channels?.filter(c => c.streamType === 'live') || [];

  const toggleFavorite = useToggleFavorite();
  const updateLastWatched = useUpdateLastWatched();

  const handleSelectChannel = useCallback((channel: Channel) => {
    setChannel(channel);
    updateLastWatched.mutate(channel.id);
  }, [setChannel, updateLastWatched]);

  const handleToggleFavorite = useCallback((channelId: string) => {
    toggleFavorite.mutate(channelId);
  }, [toggleFavorite]);

  const handleNextChannel = useCallback(() => {
    if (!currentChannel || liveChannels.length === 0) return;
    const currentIndex = liveChannels.findIndex(c => c.id === currentChannel.id);
    const nextIndex = (currentIndex + 1) % liveChannels.length;
    handleSelectChannel(liveChannels[nextIndex]);
  }, [currentChannel, liveChannels, handleSelectChannel]);

  const handlePrevChannel = useCallback(() => {
    if (!currentChannel || liveChannels.length === 0) return;
    const currentIndex = liveChannels.findIndex(c => c.id === currentChannel.id);
    const prevIndex = currentIndex === 0 ? liveChannels.length - 1 : currentIndex - 1;
    handleSelectChannel(liveChannels[prevIndex]);
  }, [currentChannel, liveChannels, handleSelectChannel]);

  return (
    <div className="h-full flex">
      {/* Player Section */}
      <motion.div
        className="flex-1 bg-black"
        animate={{ width: showChannelList ? '60%' : '100%' }}
        transition={{ duration: 0.3 }}
      >
        <VaultPlayer
          channel={currentChannel}
          onNextChannel={handleNextChannel}
          onPrevChannel={handlePrevChannel}
          onShowEPG={() => setShowChannelList(true)}
        />
      </motion.div>

      {/* Channel List */}
      {showChannelList && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="w-[40%] min-w-[320px] max-w-[500px] border-l border-vault-border bg-vault-bg"
        >
          <ChannelGrid
            channels={liveChannels}
            selectedChannelId={currentChannel?.id}
            onSelectChannel={handleSelectChannel}
            onToggleFavorite={handleToggleFavorite}
          />
        </motion.div>
      )}
    </div>
  );
}

export default LiveTV;
