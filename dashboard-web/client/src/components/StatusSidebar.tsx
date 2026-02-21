/*
 * DESIGN: "Sovereign Terminal" — Left sidebar with stacked status panels
 * Each panel has a 2px Bitcoin orange top border and monospace headers
 */

import { Activity, Bell, Zap, Users, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  AGENT_CATALOG, MOCK_HEALTH, MOCK_NOTIFICATIONS,
} from "@/lib/data";

interface StatusSidebarProps {
  onSelectAgent: (id: string) => void;
  selectedAgent: string | null;
}

export default function StatusSidebar({ onSelectAgent, selectedAgent }: StatusSidebarProps) {
  return (
    <div className="p-3 space-y-3">
      {/* System Health Panel */}
      <div className="panel">
        <div className="panel-header flex items-center gap-2">
          <Activity className="w-3 h-3" />
          <span>// SYSTEM HEALTH</span>
        </div>
        <div className="p-3 text-[12px]">
          <table className="w-full">
            <tbody>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Ollama</td>
                <td className="text-right py-1">
                  <span className="inline-flex items-center gap-1.5">
                    <span className={`status-dot ${MOCK_HEALTH.ollama === 'up' ? 'status-dot-active' : 'status-dot-danger'}`} />
                    <span className={MOCK_HEALTH.ollama === 'up' ? 'text-electric-green' : 'text-danger-red'}>
                      {MOCK_HEALTH.ollama.toUpperCase()}
                    </span>
                  </span>
                </td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Model</td>
                <td className="text-right py-1 text-foreground">{MOCK_HEALTH.model}</td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Swarm</td>
                <td className="text-right py-1">
                  <span className="inline-flex items-center gap-1.5">
                    <span className={`status-dot ${MOCK_HEALTH.swarmRegistry === 'active' ? 'status-dot-active' : 'status-dot-warning'}`} />
                    <span className={MOCK_HEALTH.swarmRegistry === 'active' ? 'text-electric-green' : 'text-warning-amber'}>
                      {MOCK_HEALTH.swarmRegistry.toUpperCase()}
                    </span>
                  </span>
                </td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Uptime</td>
                <td className="text-right py-1 text-foreground">{MOCK_HEALTH.uptime}</td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Tasks</td>
                <td className="text-right py-1 text-foreground">
                  <span className="text-electric-green">{MOCK_HEALTH.completedTasks}</span>
                  <span className="text-muted-foreground">/</span>
                  <span>{MOCK_HEALTH.totalTasks}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Agents Panel */}
      <div className="panel">
        <div className="panel-header flex items-center gap-2">
          <Users className="w-3 h-3" />
          <span>// AGENTS</span>
        </div>
        <div className="p-1">
          {AGENT_CATALOG.map((agent) => (
            <button
              key={agent.id}
              onClick={() => onSelectAgent(agent.id)}
              className={`w-full text-left px-3 py-2 flex items-center gap-2.5 text-[12px] transition-colors hover:bg-accent ${
                selectedAgent === agent.id ? 'bg-accent border-l-2 border-btc-orange' : ''
              }`}
            >
              <span className={`status-dot flex-shrink-0 ${
                agent.status === 'active' ? 'status-dot-active' :
                agent.status === 'planned' ? 'status-dot-planned' : 'status-dot-danger'
              }`} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <span className="font-medium text-foreground">{agent.name}</span>
                  {agent.rateSats > 0 && (
                    <span className="text-[10px] text-btc-orange">{agent.rateSats} sats</span>
                  )}
                </div>
                <span className="text-[10px] text-muted-foreground truncate block">
                  {agent.role}
                </span>
              </div>
              <ChevronRight className="w-3 h-3 text-muted-foreground flex-shrink-0" />
            </button>
          ))}
        </div>
      </div>

      {/* L402 Balance Panel */}
      <div className="panel">
        <div className="panel-header flex items-center gap-2">
          <Zap className="w-3 h-3" />
          <span>// L402 TREASURY</span>
        </div>
        <div className="p-3 text-[12px]">
          <div className="text-center mb-3">
            <div className="sat-amount text-[20px] font-bold">
              ₿ {MOCK_HEALTH.l402Balance.toLocaleString()}
            </div>
            <div className="text-[10px] text-muted-foreground mt-0.5">satoshis available</div>
          </div>
          <table className="w-full">
            <tbody>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Protocol</td>
                <td className="text-right py-1 text-foreground">L402 / Lightning</td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Macaroon</td>
                <td className="text-right py-1">
                  <span className="text-electric-green text-[10px] uppercase tracking-wider">Valid</span>
                </td>
              </tr>
              <tr>
                <td className="text-muted-foreground py-1 pr-2">Network</td>
                <td className="text-right py-1 text-foreground">Testnet</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Notifications Panel */}
      <div className="panel">
        <div className="panel-header flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-3 h-3" />
            <span>// NOTIFICATIONS</span>
          </div>
          <Badge variant="secondary" className="text-[9px] h-4 px-1.5 bg-btc-orange/20 text-btc-orange border-0">
            {MOCK_NOTIFICATIONS.filter(n => !n.read).length} new
          </Badge>
        </div>
        <div className="p-1">
          {MOCK_NOTIFICATIONS.slice(0, 4).map((notif) => (
            <div
              key={notif.id}
              className={`px-3 py-2 text-[11px] border-b border-border/50 last:border-0 ${
                !notif.read ? 'bg-accent/50' : ''
              }`}
            >
              <div className="flex items-center gap-1.5 mb-0.5">
                {!notif.read && <span className="w-1.5 h-1.5 rounded-full bg-btc-orange flex-shrink-0" />}
                <span className="font-medium text-foreground truncate">{notif.title}</span>
                <span className="text-[9px] text-muted-foreground ml-auto flex-shrink-0">
                  {getCategoryIcon(notif.category)}
                </span>
              </div>
              <p className="text-muted-foreground truncate pl-3">{notif.message}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function getCategoryIcon(category: string): string {
  switch (category) {
    case "swarm": return "⚡";
    case "task": return "📋";
    case "agent": return "🤖";
    case "system": return "⚙️";
    case "payment": return "₿";
    default: return "•";
  }
}
