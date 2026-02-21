/*
 * DESIGN: "Sovereign Terminal" — Agent Marketplace
 * Browse agents, see capabilities, hire with sats
 * Lightning payment visualization as hero
 */

import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AGENT_CATALOG, type Agent } from "@/lib/data";
import { motion } from "framer-motion";
import { Store, Zap, ChevronRight } from "lucide-react";
import { toast } from "sonner";

const LIGHTNING_IMG = "https://private-us-east-1.manuscdn.com/sessionFile/hmEvCGQLHKyGnx6qwMSEHn/sandbox/qiXHjJUmj8lqJymwhLI5B2-img-3_1771695706000_na1fn_bGlnaHRuaW5nLXBheW1lbnQ.png?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvaG1FdkNHUUxIS3lHbng2cXdNU0VIbi9zYW5kYm94L3FpWEhqSlVtajhscUp5bXdoTEk1QjItaW1nLTNfMTc3MTY5NTcwNjAwMF9uYTFmbl9iR2xuYUhSdWFXNW5MWEJoZVcxbGJuUS5wbmc~eC1vc3MtcHJvY2Vzcz1pbWFnZS9yZXNpemUsd18xOTIwLGhfMTkyMC9mb3JtYXQsd2VicC9xdWFsaXR5LHFfODAiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE3OTg3NjE2MDB9fX1dfQ__&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=gWuDcQJeJeaEupkqbE5tOSIOgB6A2LjDuU7w6nK8RzOSmeWWy~4AJVsm68hi--j22DFlv7hDWhZnoQ9WdyU0oCn3tIUFPaaamtcUY-9qBE3yw9VjAnBRJjG3ppnfVSFY-KaVvuX2hjkgzeknhsEmSuIo55yL6Y8c4CwsoVeLW7AloD9ou-2xBEKNObQqwRG~FP~cMMLOyNoPDzwclB8B~Imm3Qd~0-LAfKDp0nksbpBV87IN8YKsFxyAV5Bq~Mm-wqlGJZwBGzYfOPQQUNaTYZ2zzIidxTMNDLUE70fgc~oI2~0i2ebq-~8QFJwuLywTVycxV61BKssTsiOMBizE0g__";

interface MarketplacePanelProps {
  onSelectAgent: (id: string) => void;
}

export default function MarketplacePanel({ onSelectAgent }: MarketplacePanelProps) {
  return (
    <ScrollArea className="h-full">
      <div className="p-4">
        {/* Hero banner */}
        <div className="relative h-[200px] overflow-hidden mb-6 border border-border"
          style={{ borderTop: '2px solid oklch(0.75 0.18 55)' }}
        >
          <img
            src={LIGHTNING_IMG}
            alt="Lightning Network"
            className="w-full h-full object-cover opacity-60"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/60 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <div className="text-[11px] uppercase tracking-[0.15em] text-btc-orange mb-1">
              // AGENT MARKETPLACE
            </div>
            <p className="text-[13px] text-foreground max-w-md leading-relaxed">
              Hire specialized agents with Lightning sats. Each agent bids on tasks
              through the L402 auction system. No API keys — just sats.
            </p>
          </div>
        </div>

        {/* Agent catalog */}
        <div className="text-[11px] uppercase tracking-[0.15em] text-muted-foreground mb-3">
          // AVAILABLE AGENTS
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {AGENT_CATALOG.map((agent, i) => (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="panel p-4 hover:bg-panel-hover transition-colors group"
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className={`status-dot ${
                      agent.status === 'active' ? 'status-dot-active' : 'status-dot-planned'
                    }`} />
                    <span className="text-[14px] font-semibold text-foreground">{agent.name}</span>
                  </div>
                  <span className="text-[11px] text-muted-foreground">{agent.role}</span>
                </div>
                <div className="text-right">
                  {agent.rateSats === 0 ? (
                    <Badge variant="outline" className="text-[9px] border-electric-green/30 text-electric-green">
                      FREE
                    </Badge>
                  ) : (
                    <div className="flex items-center gap-1">
                      <Zap className="w-3 h-3 text-btc-orange" />
                      <span className="sat-amount text-[13px]">{agent.rateSats}</span>
                      <span className="text-[9px] text-muted-foreground">sats/task</span>
                    </div>
                  )}
                </div>
              </div>

              <p className="text-[11px] text-muted-foreground leading-relaxed mb-3">
                {agent.description}
              </p>

              <div className="flex flex-wrap gap-1 mb-3">
                {agent.capabilities.map(cap => (
                  <span key={cap} className="text-[9px] px-1.5 py-0.5 bg-accent text-accent-foreground border border-border">
                    {cap}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between">
                <Badge
                  variant="outline"
                  className={`text-[9px] ${
                    agent.status === 'active'
                      ? 'border-electric-green/30 text-electric-green'
                      : 'border-muted-foreground/30 text-muted-foreground'
                  }`}
                >
                  {agent.status.toUpperCase()}
                </Badge>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 text-[10px] text-btc-orange hover:text-btc-orange/80 hover:bg-btc-orange/10 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => {
                    if (agent.status === 'active') {
                      onSelectAgent(agent.id);
                    } else {
                      toast("Agent not yet available", {
                        description: `${agent.name} is planned for a future release.`,
                      });
                    }
                  }}
                >
                  {agent.status === 'active' ? 'VIEW' : 'COMING SOON'}
                  <ChevronRight className="w-3 h-3 ml-1" />
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </ScrollArea>
  );
}
