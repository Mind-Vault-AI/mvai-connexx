// ============================================
// VAULT TV - Channel Card Component
// ============================================

import { motion } from 'framer-motion';
import { Heart, Play } from 'lucide-react';
import { cn } from '../../utils/cn';
import type { Channel } from '../../types';

interface ChannelCardProps {
  channel: Channel;
  isActive?: boolean;
  onSelect: (channel: Channel) => void;
  onToggleFavorite?: (channelId: string) => void;
}

export function ChannelCard({
  channel,
  isActive = false,
  onSelect,
  onToggleFavorite
}: ChannelCardProps) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onSelect(channel)}
      className={cn(
        'relative group cursor-pointer rounded-lg overflow-hidden',
        'bg-vault-surface border border-vault-border',
        'transition-all duration-200',
        isActive && 'ring-2 ring-vault-primary border-vault-primary'
      )}
    >
      {/* Thumbnail/Logo */}
      <div className="aspect-video bg-vault-elevated flex items-center justify-center relative">
        {channel.logoUrl ? (
          <img
            src={channel.logoUrl}
            alt={channel.name}
            className="w-full h-full object-contain p-4"
            loading="lazy"
          />
        ) : (
          <div className="w-16 h-16 rounded-full bg-vault-border flex items-center justify-center">
            <span className="text-2xl font-bold text-vault-text-muted">
              {channel.name.charAt(0).toUpperCase()}
            </span>
          </div>
        )}

        {/* Play Overlay */}
        <div
          className={cn(
            'absolute inset-0 bg-black/60 flex items-center justify-center',
            'opacity-0 group-hover:opacity-100 transition-opacity'
          )}
        >
          <div className="w-14 h-14 rounded-full bg-vault-primary flex items-center justify-center">
            <Play className="w-7 h-7 text-white ml-1" fill="white" />
          </div>
        </div>

        {/* Live Badge */}
        {channel.streamType === 'live' && (
          <div className="absolute top-2 left-2 px-2 py-0.5 bg-vault-primary rounded text-xs font-medium text-white">
            LIVE
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-3">
        <h3 className="font-medium text-white truncate" title={channel.name}>
          {channel.name}
        </h3>
        <p className="text-sm text-vault-text-muted truncate mt-0.5">
          {channel.groupTitle}
        </p>
      </div>

      {/* Favorite Button */}
      {onToggleFavorite && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleFavorite(channel.id);
          }}
          className={cn(
            'absolute top-2 right-2 p-2 rounded-full transition-all',
            'opacity-0 group-hover:opacity-100',
            channel.isFavorite
              ? 'bg-vault-primary text-white opacity-100'
              : 'bg-black/60 text-white hover:bg-vault-primary'
          )}
        >
          <Heart
            className="w-4 h-4"
            fill={channel.isFavorite ? 'currentColor' : 'none'}
          />
        </button>
      )}
    </motion.div>
  );
}

export default ChannelCard;
