// ============================================
// VAULT TV - Sidebar Component
// ============================================

import { motion } from 'framer-motion';
import {
  Tv,
  Film,
  Clapperboard,
  Heart,
  Clock,
  Settings,
  ChevronLeft,
  ChevronRight,
  Plus,
  Zap
} from 'lucide-react';
import { cn } from '../../utils/cn';
import { useAppStore } from '../../stores/appStore';
import { usePremiumFeatures } from '../../hooks/usePremiumFeatures';
import type { ViewType } from '../../types';

interface NavItem {
  id: ViewType;
  label: string;
  icon: React.ElementType;
  premiumOnly?: boolean;
}

const navItems: NavItem[] = [
  { id: 'live', label: 'Live TV', icon: Tv },
  { id: 'movies', label: 'Movies', icon: Film },
  { id: 'series', label: 'Series', icon: Clapperboard },
  { id: 'favorites', label: 'Favorites', icon: Heart },
  { id: 'recordings', label: 'Recordings', icon: Clock, premiumOnly: true },
  { id: 'settings', label: 'Settings', icon: Settings }
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar, currentView, setCurrentView } = useAppStore();
  const { isPremium, plan } = usePremiumFeatures();

  return (
    <motion.aside
      initial={false}
      animate={{ width: sidebarCollapsed ? 72 : 240 }}
      className="h-full bg-vault-surface border-r border-vault-border flex flex-col"
    >
      {/* Logo */}
      <div className="h-16 flex items-center px-4 border-b border-vault-border">
        <motion.div
          className="flex items-center gap-3 overflow-hidden"
          animate={{ justifyContent: sidebarCollapsed ? 'center' : 'flex-start' }}
        >
          <div className="w-10 h-10 bg-vault-primary rounded-lg flex items-center justify-center flex-shrink-0">
            <Zap className="w-6 h-6 text-white" />
          </div>
          {!sidebarCollapsed && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="font-bold text-xl text-white whitespace-nowrap"
            >
              Vault TV
            </motion.span>
          )}
        </motion.div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const isActive = currentView === item.id;
          const isLocked = item.premiumOnly && !isPremium;

          return (
            <button
              key={item.id}
              onClick={() => !isLocked && setCurrentView(item.id)}
              className={cn(
                'w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-all',
                isActive
                  ? 'bg-vault-primary text-white'
                  : 'text-vault-text-muted hover:bg-vault-elevated hover:text-white',
                isLocked && 'opacity-50 cursor-not-allowed'
              )}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {!sidebarCollapsed && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="whitespace-nowrap"
                >
                  {item.label}
                </motion.span>
              )}
              {!sidebarCollapsed && isLocked && (
                <span className="ml-auto text-xs bg-vault-primary/20 text-vault-primary px-2 py-0.5 rounded">
                  PRO
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Add Provider Button */}
      <div className="p-2 border-t border-vault-border">
        <button
          onClick={() => setCurrentView('settings')}
          className={cn(
            'w-full flex items-center gap-3 px-3 py-3 rounded-lg',
            'bg-vault-elevated hover:bg-vault-border transition-colors',
            'text-vault-text-muted hover:text-white'
          )}
        >
          <Plus className="w-5 h-5 flex-shrink-0" />
          {!sidebarCollapsed && <span>Add Playlist</span>}
        </button>
      </div>

      {/* Premium Badge */}
      {!sidebarCollapsed && (
        <div className="p-4 border-t border-vault-border">
          <div
            className={cn(
              'p-3 rounded-lg',
              isPremium ? 'bg-vault-accent/10' : 'bg-vault-primary/10'
            )}
          >
            <p className="text-sm font-medium text-white">
              {isPremium ? 'Premium Active' : 'Free Plan'}
            </p>
            <p className="text-xs text-vault-text-muted mt-1">
              {isPremium ? `${plan.charAt(0).toUpperCase() + plan.slice(1)} Plan` : 'Upgrade for more features'}
            </p>
          </div>
        </div>
      )}

      {/* Collapse Toggle */}
      <button
        onClick={toggleSidebar}
        className="h-12 flex items-center justify-center border-t border-vault-border text-vault-text-muted hover:text-white transition-colors"
      >
        {sidebarCollapsed ? (
          <ChevronRight className="w-5 h-5" />
        ) : (
          <ChevronLeft className="w-5 h-5" />
        )}
      </button>
    </motion.aside>
  );
}

export default Sidebar;
