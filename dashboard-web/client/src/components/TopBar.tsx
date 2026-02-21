/*
 * DESIGN: "Sovereign Terminal" — Top navigation bar
 * Bitcoin orange accent line at top, system title, notification bell
 */

import { Bell, Menu, Terminal, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MOCK_HEALTH } from "@/lib/data";

interface TopBarProps {
  unreadCount: number;
  onToggleSidebar: () => void;
}

export default function TopBar({ unreadCount, onToggleSidebar }: TopBarProps) {
  return (
    <header className="h-12 flex-shrink-0 border-b border-border bg-card flex items-center px-4 gap-3"
      style={{ borderTop: '2px solid oklch(0.75 0.18 55)' }}
    >
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden h-8 w-8 text-muted-foreground hover:text-foreground"
        onClick={onToggleSidebar}
      >
        <Menu className="w-4 h-4" />
      </Button>

      {/* Logo / Title */}
      <div className="flex items-center gap-2">
        <Terminal className="w-4 h-4 text-btc-orange" />
        <span className="text-[13px] font-semibold tracking-[0.05em] text-foreground">
          TIMMY TIME
        </span>
        <span className="text-[10px] text-muted-foreground tracking-[0.1em]">
          MISSION CONTROL
        </span>
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Status indicators */}
      <div className="hidden sm:flex items-center gap-4 text-[11px] text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <span className={`status-dot ${MOCK_HEALTH.ollama === 'up' ? 'status-dot-active' : 'status-dot-danger'}`} />
          <span>OLLAMA</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className={`status-dot ${MOCK_HEALTH.swarmRegistry === 'active' ? 'status-dot-active' : 'status-dot-warning'}`} />
          <span>SWARM</span>
        </div>
        <div className="flex items-center gap-1.5">
          <Zap className="w-3 h-3 text-btc-orange" />
          <span className="text-btc-orange font-medium">
            {MOCK_HEALTH.l402Balance.toLocaleString()} sats
          </span>
        </div>
      </div>

      {/* Notifications */}
      <Button
        variant="ghost"
        size="icon"
        className="relative h-8 w-8 text-muted-foreground hover:text-foreground"
      >
        <Bell className="w-4 h-4" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 w-4 h-4 rounded-full bg-btc-orange text-[9px] font-bold text-black flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </Button>

      {/* Version */}
      <span className="text-[9px] text-muted-foreground tracking-wider hidden md:inline">
        v2.0.0
      </span>
    </header>
  );
}
