// ============================================
// VAULT TV - Settings View
// ============================================

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Plus,
  Trash2,
  RefreshCw,
  Link,
  User,
  Lock,
  Server,
  Shield,
  Zap,
  ExternalLink
} from 'lucide-react';
import { useProviders } from '../hooks/useProviders';
import { useAddProvider, useSyncProvider } from '../hooks/useChannels';
import { usePremiumFeatures } from '../hooks/usePremiumFeatures';
import { cn } from '../utils/cn';
import { playlistManager } from '../services/PlaylistManager';
import type { ProviderConfig } from '../types';

type ProviderType = 'xtream' | 'm3u';

export function Settings() {
  const providers = useProviders();
  const addProvider = useAddProvider();
  const syncProvider = useSyncProvider();
  const { isPremium, plan, limits } = usePremiumFeatures();

  const [showAddModal, setShowAddModal] = useState(false);
  const [providerType, setProviderType] = useState<ProviderType>('xtream');
  const [formData, setFormData] = useState({
    name: '',
    serverUrl: '',
    username: '',
    password: '',
    m3uUrl: '',
    epgUrl: ''
  });

  const handleAddProvider = async () => {
    let config: ProviderConfig;

    if (providerType === 'xtream') {
      config = {
        type: 'xtream',
        serverUrl: formData.serverUrl,
        username: formData.username,
        password: formData.password,
        name: formData.name || undefined
      };
    } else {
      config = {
        type: 'm3u',
        url: formData.m3uUrl,
        name: formData.name || undefined,
        epgUrl: formData.epgUrl || undefined
      };
    }

    await addProvider.mutateAsync(config);
    setShowAddModal(false);
    setFormData({ name: '', serverUrl: '', username: '', password: '', m3uUrl: '', epgUrl: '' });
  };

  const handleRemoveProvider = async (providerId: string) => {
    if (confirm('Are you sure you want to remove this playlist?')) {
      await playlistManager.removeProvider(providerId);
    }
  };

  const canAddProvider = !limits || providers.length < limits.maxPlaylists;

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-4xl mx-auto p-6 space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Settings</h1>
          <p className="text-vault-text-muted mt-1">Manage your playlists and preferences</p>
        </div>

        {/* Playlists Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Playlists</h2>
            <button
              onClick={() => setShowAddModal(true)}
              disabled={!canAddProvider}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                canAddProvider
                  ? 'bg-vault-primary hover:bg-vault-primary-hover text-white'
                  : 'bg-vault-elevated text-vault-text-muted cursor-not-allowed'
              )}
            >
              <Plus className="w-4 h-4" />
              Add Playlist
            </button>
          </div>

          {!canAddProvider && (
            <div className="p-4 bg-vault-primary/10 border border-vault-primary/20 rounded-lg">
              <p className="text-sm text-vault-primary">
                Free plan limited to {limits?.maxPlaylists} playlist. Upgrade to Premium for unlimited playlists.
              </p>
            </div>
          )}

          {/* Provider List */}
          <div className="space-y-3">
            {providers.map((provider) => (
              <motion.div
                key={provider.id}
                layout
                className="p-4 bg-vault-surface border border-vault-border rounded-lg"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      'w-3 h-3 rounded-full',
                      provider.status === 'active' && 'bg-vault-accent',
                      provider.status === 'syncing' && 'bg-yellow-500 animate-pulse',
                      provider.status === 'error' && 'bg-vault-primary',
                      provider.status === 'offline' && 'bg-vault-text-muted'
                    )} />
                    <div>
                      <h3 className="font-medium text-white">{provider.name}</h3>
                      <p className="text-sm text-vault-text-muted">
                        {provider.channelCount} channels • {provider.config.type.toUpperCase()}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => syncProvider.mutate(provider.id)}
                      disabled={provider.status === 'syncing'}
                      className="p-2 text-vault-text-muted hover:text-white transition-colors"
                      title="Refresh"
                    >
                      <RefreshCw className={cn('w-4 h-4', provider.status === 'syncing' && 'animate-spin')} />
                    </button>
                    <button
                      onClick={() => handleRemoveProvider(provider.id)}
                      className="p-2 text-vault-text-muted hover:text-vault-primary transition-colors"
                      title="Remove"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}

            {providers.length === 0 && (
              <div className="p-8 text-center text-vault-text-muted bg-vault-surface border border-vault-border rounded-lg">
                <Server className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p>No playlists added yet</p>
                <p className="text-sm mt-1">Add your first playlist to start watching</p>
              </div>
            )}
          </div>
        </section>

        {/* Integrations Section */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-white">Integrations</h2>

          <div className="grid gap-4 sm:grid-cols-2">
            {/* Real-Debrid */}
            <div className="p-4 bg-vault-surface border border-vault-border rounded-lg">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-green-500/10 rounded-lg flex items-center justify-center">
                  <Zap className="w-5 h-5 text-green-500" />
                </div>
                <div>
                  <h3 className="font-medium text-white">Real-Debrid</h3>
                  <p className="text-xs text-vault-text-muted">Premium link unrestricting</p>
                </div>
              </div>
              <button className="w-full py-2 px-4 bg-vault-elevated hover:bg-vault-border text-white rounded-lg transition-colors flex items-center justify-center gap-2">
                <ExternalLink className="w-4 h-4" />
                Connect
              </button>
            </div>

            {/* VPN */}
            <div className="p-4 bg-vault-surface border border-vault-border rounded-lg">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 bg-blue-500/10 rounded-lg flex items-center justify-center">
                  <Shield className="w-5 h-5 text-blue-500" />
                </div>
                <div>
                  <h3 className="font-medium text-white">VPN Protection</h3>
                  <p className="text-xs text-vault-text-muted">Secure your connection</p>
                </div>
              </div>
              <button className="w-full py-2 px-4 bg-vault-elevated hover:bg-vault-border text-white rounded-lg transition-colors flex items-center justify-center gap-2">
                <ExternalLink className="w-4 h-4" />
                Setup
              </button>
            </div>
          </div>
        </section>

        {/* Premium Section */}
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-white">Subscription</h2>

          <div className={cn(
            'p-6 rounded-xl',
            isPremium
              ? 'bg-gradient-to-br from-vault-accent/20 to-vault-accent/5 border border-vault-accent/30'
              : 'bg-gradient-to-br from-vault-primary/20 to-vault-primary/5 border border-vault-primary/30'
          )}>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-white">
                  {isPremium ? `${plan.charAt(0).toUpperCase() + plan.slice(1)} Plan` : 'Free Plan'}
                </h3>
                <p className="text-vault-text-muted">
                  {isPremium ? 'All features unlocked' : 'Limited features'}
                </p>
              </div>
              {!isPremium && (
                <button className="px-6 py-2.5 bg-vault-primary hover:bg-vault-primary-hover text-white font-medium rounded-lg transition-colors">
                  Upgrade to Premium
                </button>
              )}
            </div>

            {!isPremium && (
              <ul className="space-y-2 text-sm">
                <li className="flex items-center gap-2 text-vault-text-muted">
                  <span className="text-vault-primary">✗</span> Multi-view (Picture-in-Picture)
                </li>
                <li className="flex items-center gap-2 text-vault-text-muted">
                  <span className="text-vault-primary">✗</span> Cloud DVR Recording
                </li>
                <li className="flex items-center gap-2 text-vault-text-muted">
                  <span className="text-vault-primary">✗</span> 4K Upscaling
                </li>
                <li className="flex items-center gap-2 text-vault-text-muted">
                  <span className="text-vault-primary">✗</span> AI-Powered Search
                </li>
              </ul>
            )}
          </div>
        </section>
      </div>

      {/* Add Provider Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-md bg-vault-surface border border-vault-border rounded-xl p-6"
          >
            <h2 className="text-xl font-bold text-white mb-4">Add Playlist</h2>

            {/* Type Selector */}
            <div className="flex gap-2 mb-4">
              <button
                onClick={() => setProviderType('xtream')}
                className={cn(
                  'flex-1 py-2 rounded-lg transition-colors',
                  providerType === 'xtream'
                    ? 'bg-vault-primary text-white'
                    : 'bg-vault-elevated text-vault-text-muted'
                )}
              >
                Xtream Codes
              </button>
              <button
                onClick={() => setProviderType('m3u')}
                className={cn(
                  'flex-1 py-2 rounded-lg transition-colors',
                  providerType === 'm3u'
                    ? 'bg-vault-primary text-white'
                    : 'bg-vault-elevated text-vault-text-muted'
                )}
              >
                M3U URL
              </button>
            </div>

            {/* Form */}
            <div className="space-y-3">
              <div>
                <label className="block text-sm text-vault-text-muted mb-1">Name (optional)</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData(f => ({ ...f, name: e.target.value }))}
                  placeholder="My Playlist"
                  className="w-full px-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                />
              </div>

              {providerType === 'xtream' ? (
                <>
                  <div>
                    <label className="block text-sm text-vault-text-muted mb-1">Server URL</label>
                    <div className="relative">
                      <Server className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-vault-text-muted" />
                      <input
                        type="url"
                        value={formData.serverUrl}
                        onChange={(e) => setFormData(f => ({ ...f, serverUrl: e.target.value }))}
                        placeholder="http://example.com:8080"
                        className="w-full pl-10 pr-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm text-vault-text-muted mb-1">Username</label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-vault-text-muted" />
                      <input
                        type="text"
                        value={formData.username}
                        onChange={(e) => setFormData(f => ({ ...f, username: e.target.value }))}
                        placeholder="username"
                        className="w-full pl-10 pr-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm text-vault-text-muted mb-1">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-vault-text-muted" />
                      <input
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData(f => ({ ...f, password: e.target.value }))}
                        placeholder="••••••••"
                        className="w-full pl-10 pr-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                      />
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <div>
                    <label className="block text-sm text-vault-text-muted mb-1">M3U URL</label>
                    <div className="relative">
                      <Link className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-vault-text-muted" />
                      <input
                        type="url"
                        value={formData.m3uUrl}
                        onChange={(e) => setFormData(f => ({ ...f, m3uUrl: e.target.value }))}
                        placeholder="http://example.com/playlist.m3u"
                        className="w-full pl-10 pr-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm text-vault-text-muted mb-1">EPG URL (optional)</label>
                    <div className="relative">
                      <Link className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-vault-text-muted" />
                      <input
                        type="url"
                        value={formData.epgUrl}
                        onChange={(e) => setFormData(f => ({ ...f, epgUrl: e.target.value }))}
                        placeholder="http://example.com/epg.xml"
                        className="w-full pl-10 pr-4 py-2.5 bg-vault-elevated border border-vault-border rounded-lg text-white placeholder-vault-text-muted focus:outline-none focus:border-vault-primary"
                      />
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Actions */}
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="flex-1 py-2.5 bg-vault-elevated hover:bg-vault-border text-white rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleAddProvider}
                disabled={addProvider.isPending}
                className="flex-1 py-2.5 bg-vault-primary hover:bg-vault-primary-hover text-white rounded-lg transition-colors disabled:opacity-50"
              >
                {addProvider.isPending ? 'Adding...' : 'Add Playlist'}
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}

export default Settings;
