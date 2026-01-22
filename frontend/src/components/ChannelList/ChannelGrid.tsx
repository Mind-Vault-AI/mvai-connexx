// ============================================
// VAULT TV - Channel Grid Component
// ============================================

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, Grid, List, Loader2 } from 'lucide-react';
import { ChannelCard } from './ChannelCard';
import { cn } from '../../utils/cn';
import type { Channel, Category } from '../../types';

interface ChannelGridProps {
  channels: Channel[];
  categories?: Category[];
  isLoading?: boolean;
  selectedChannelId?: string | null;
  onSelectChannel: (channel: Channel) => void;
  onToggleFavorite?: (channelId: string) => void;
}

export function ChannelGrid({
  channels,
  categories = [],
  isLoading = false,
  selectedChannelId,
  onSelectChannel,
  onToggleFavorite
}: ChannelGridProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Filter channels
  const filteredChannels = useMemo(() => {
    let result = channels;

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      result = result.filter(
        (ch) =>
          ch.name.toLowerCase().includes(query) ||
          ch.groupTitle.toLowerCase().includes(query)
      );
    }

    if (selectedCategory) {
      result = result.filter((ch) => ch.groupTitle === selectedCategory);
    }

    return result;
  }, [channels, searchQuery, selectedCategory]);

  // Get unique categories from channels
  const uniqueCategories = useMemo(() => {
    const cats = new Set(channels.map((ch) => ch.groupTitle));
    return Array.from(cats).sort();
  }, [channels]);

  if (isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-vault-primary" />
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header Controls */}
      <div className="p-4 border-b border-vault-border space-y-3">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-vault-text-muted" />
          <input
            type="text"
            placeholder="Search channels..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className={cn(
              'w-full pl-10 pr-4 py-2.5 rounded-lg',
              'bg-vault-elevated border border-vault-border',
              'text-white placeholder-vault-text-muted',
              'focus:outline-none focus:border-vault-primary',
              'transition-colors'
            )}
          />
        </div>

        {/* Category Filter & View Toggle */}
        <div className="flex items-center gap-3">
          <div className="flex-1 flex items-center gap-2 overflow-x-auto pb-1 scrollbar-hide">
            <button
              onClick={() => setSelectedCategory(null)}
              className={cn(
                'px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors',
                !selectedCategory
                  ? 'bg-vault-primary text-white'
                  : 'bg-vault-elevated text-vault-text-muted hover:text-white'
              )}
            >
              All
            </button>
            {uniqueCategories.slice(0, 10).map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={cn(
                  'px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors',
                  selectedCategory === cat
                    ? 'bg-vault-primary text-white'
                    : 'bg-vault-elevated text-vault-text-muted hover:text-white'
                )}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* View Toggle */}
          <div className="flex items-center bg-vault-elevated rounded-lg p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={cn(
                'p-1.5 rounded',
                viewMode === 'grid'
                  ? 'bg-vault-primary text-white'
                  : 'text-vault-text-muted hover:text-white'
              )}
            >
              <Grid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={cn(
                'p-1.5 rounded',
                viewMode === 'list'
                  ? 'bg-vault-primary text-white'
                  : 'text-vault-text-muted hover:text-white'
              )}
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Channel Count */}
      <div className="px-4 py-2 text-sm text-vault-text-muted">
        {filteredChannels.length} channels
        {selectedCategory && ` in ${selectedCategory}`}
      </div>

      {/* Channel Grid/List */}
      <div className="flex-1 overflow-y-auto p-4">
        {filteredChannels.length === 0 ? (
          <div className="h-full flex items-center justify-center text-vault-text-muted">
            No channels found
          </div>
        ) : viewMode === 'grid' ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
            <AnimatePresence mode="popLayout">
              {filteredChannels.map((channel) => (
                <ChannelCard
                  key={channel.id}
                  channel={channel}
                  isActive={channel.id === selectedChannelId}
                  onSelect={onSelectChannel}
                  onToggleFavorite={onToggleFavorite}
                />
              ))}
            </AnimatePresence>
          </div>
        ) : (
          <div className="space-y-2">
            <AnimatePresence mode="popLayout">
              {filteredChannels.map((channel) => (
                <ChannelListItem
                  key={channel.id}
                  channel={channel}
                  isActive={channel.id === selectedChannelId}
                  onSelect={onSelectChannel}
                  onToggleFavorite={onToggleFavorite}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}

// List view item
function ChannelListItem({
  channel,
  isActive,
  onSelect,
  onToggleFavorite
}: {
  channel: Channel;
  isActive: boolean;
  onSelect: (channel: Channel) => void;
  onToggleFavorite?: (channelId: string) => void;
}) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      onClick={() => onSelect(channel)}
      className={cn(
        'flex items-center gap-4 p-3 rounded-lg cursor-pointer',
        'bg-vault-surface border border-vault-border',
        'hover:bg-vault-elevated transition-colors',
        isActive && 'ring-2 ring-vault-primary border-vault-primary'
      )}
    >
      {/* Logo */}
      <div className="w-12 h-12 rounded bg-vault-elevated flex items-center justify-center flex-shrink-0">
        {channel.logoUrl ? (
          <img
            src={channel.logoUrl}
            alt=""
            className="w-full h-full object-contain p-1"
          />
        ) : (
          <span className="text-lg font-bold text-vault-text-muted">
            {channel.name.charAt(0)}
          </span>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <h3 className="font-medium text-white truncate">{channel.name}</h3>
        <p className="text-sm text-vault-text-muted truncate">{channel.groupTitle}</p>
      </div>

      {/* Number */}
      {channel.number && (
        <span className="text-vault-text-muted text-sm">#{channel.number}</span>
      )}
    </motion.div>
  );
}

export default ChannelGrid;
