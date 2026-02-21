/*
 * DESIGN: "Sovereign Terminal" — Swarm management panel
 * Shows agent constellation visualization and live event feed
 */

import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { AGENT_CATALOG, MOCK_WS_EVENTS, type Agent } from "@/lib/data";
import { motion } from "framer-motion";
import { Network, Radio, Zap } from "lucide-react";

const SWARM_IMG = "https://private-us-east-1.manuscdn.com/sessionFile/hmEvCGQLHKyGnx6qwMSEHn/sandbox/qiXHjJUmj8lqJymwhLI5B2-img-2_1771695716000_na1fn_c3dhcm0tbmV0d29yaw.png?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvaG1FdkNHUUxIS3lHbng2cXdNU0VIbi9zYW5kYm94L3FpWEhqSlVtajhscUp5bXdoTEk1QjItaW1nLTJfMTc3MTY5NTcxNjAwMF9uYTFmbl9jM2RoY20wdGJtVjBkMjl5YXcucG5nP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLHdfMTkyMCxoXzE5MjAvZm9ybWF0LHdlYnAvcXVhbGl0eSxxXzgwIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=rJ6lQ-h3pSQDDcUkGSTmXY2409jDYW2LdC9FU2ifVTnfppMXRrupq2SRC4e5P~Q5zx2r1ckGCWAi954bOr62u43lAXcxXn-FbW7PPVhoh3hx2LqGQrPLbSNbMw0-2AYO~4iKbUa~7igW2XdxeErPWs-fNzAfukvyh84cIAroFaLTdRT3IZR0amkWG8KSg5WWvv80lv0fO-zthT6kZDfPrSAHg0Opvtzy00ll~0lPq8V69DK3BP51GxIBiUPShjD1WgSrJsLbB7TLpug5PgTeeBRx80W0I6HIVxmRWQBOdmM~ziHQyNs8EhtCD7lYks8izHxCquCsFTuflp9IdrCIAQ__";

interface SwarmPanelProps {
  onSelectAgent: (id: string) => void;
}

export default function SwarmPanel({ onSelectAgent }: SwarmPanelProps) {
  const activeAgents = AGENT_CATALOG.filter(a => a.status === "active");
  const plannedAgents = AGENT_CATALOG.filter(a => a.status === "planned");

  return (
    <div className="h-full flex flex-col lg:flex-row">
      {/* Swarm visualization */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Network image */}
        <div className="relative h-[300px] lg:h-[400px] overflow-hidden border-b border-border">
          <img
            src={SWARM_IMG}
            alt="Swarm Network Topology"
            className="w-full h-full object-cover opacity-70"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-transparent" />
          <div className="absolute bottom-4 left-4 right-4">
            <div className="text-[11px] uppercase tracking-[0.15em] text-btc-orange mb-1">
              // SWARM TOPOLOGY
            </div>
            <div className="flex items-center gap-4 text-[11px] text-muted-foreground">
              <span className="flex items-center gap-1">
                <span className="status-dot status-dot-active" />
                {activeAgents.length} active
              </span>
              <span className="flex items-center gap-1">
                <span className="status-dot status-dot-planned" />
                {plannedAgents.length} planned
              </span>
              <span className="flex items-center gap-1">
                <Network className="w-3 h-3" />
                {AGENT_CATALOG.length} total
              </span>
            </div>
          </div>
        </div>

        {/* Agent grid */}
        <ScrollArea className="flex-1">
          <div className="p-4">
            <div className="text-[11px] uppercase tracking-[0.15em] text-muted-foreground mb-3">
              // REGISTERED AGENTS
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {AGENT_CATALOG.map((agent, i) => (
                <motion.button
                  key={agent.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => onSelectAgent(agent.id)}
                  className="panel text-left p-3 hover:bg-panel-hover transition-colors"
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`status-dot ${
                      agent.status === 'active' ? 'status-dot-active' : 'status-dot-planned'
                    }`} />
                    <span className="text-[12px] font-semibold text-foreground">{agent.name}</span>
                    <Badge variant="outline" className="text-[9px] h-4 px-1.5 border-border ml-auto">
                      {agent.status}
                    </Badge>
                  </div>
                  <div className="text-[10px] text-muted-foreground mb-1.5">{agent.role}</div>
                  <div className="flex flex-wrap gap-1">
                    {agent.capabilities.map(cap => (
                      <span key={cap} className="text-[9px] px-1.5 py-0.5 bg-accent text-accent-foreground">
                        {cap}
                      </span>
                    ))}
                  </div>
                </motion.button>
              ))}
            </div>
          </div>
        </ScrollArea>
      </div>

      {/* Live event feed */}
      <div className="lg:w-[300px] border-t lg:border-t-0 lg:border-l border-border flex flex-col">
        <div className="panel-header flex items-center gap-2">
          <Radio className="w-3 h-3 text-electric-green" />
          // LIVE FEED
          <span className="ml-auto flex items-center gap-1 text-electric-green">
            <span className="w-1.5 h-1.5 rounded-full bg-electric-green animate-pulse" />
            LIVE
          </span>
        </div>
        <ScrollArea className="flex-1 max-h-[300px] lg:max-h-none">
          <div className="p-2 space-y-1">
            {[...MOCK_WS_EVENTS].reverse().map((evt, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.03 }}
                className="px-3 py-2 text-[11px] border-b border-border/30"
              >
                <div className="flex items-center gap-1.5 mb-0.5">
                  <span className={`text-[9px] font-semibold uppercase ${getEventColor(evt.event)}`}>
                    {evt.event.replace(/_/g, ' ')}
                  </span>
                  <span className="text-[9px] text-muted-foreground ml-auto">
                    {new Date(evt.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="text-muted-foreground text-[10px]">
                  {formatEventData(evt)}
                </div>
              </motion.div>
            ))}
          </div>
        </ScrollArea>
      </div>
    </div>
  );
}

function getEventColor(event: string): string {
  if (event.includes('completed')) return 'text-electric-green';
  if (event.includes('assigned')) return 'text-btc-orange';
  if (event.includes('bid')) return 'text-warning-amber';
  if (event.includes('joined')) return 'text-cyber-cyan';
  if (event.includes('posted')) return 'text-foreground';
  return 'text-muted-foreground';
}

function formatEventData(evt: { event: string; data: Record<string, unknown> }): string {
  const d = evt.data;
  if (evt.event === 'agent_joined') return `${d.name} joined the swarm`;
  if (evt.event === 'task_posted') return `"${d.description}"`;
  if (evt.event === 'task_assigned') return `→ ${d.agent_id}`;
  if (evt.event === 'task_completed') return `✓ ${d.agent_id}: ${d.result}`;
  if (evt.event === 'bid_submitted') return `${d.agent_id} bid ${d.bid_sats} sats`;
  return JSON.stringify(d);
}
