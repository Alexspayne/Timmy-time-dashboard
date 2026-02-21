/*
 * DESIGN: "Sovereign Terminal" — Right context panel
 * Shows details for selected agent or task, voice NLU, or roadmap
 */

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  AGENT_CATALOG, MOCK_TASKS, VOICE_INTENTS, ROADMAP,
  type Agent, type Task
} from "@/lib/data";
import { motion } from "framer-motion";
import {
  User, Zap, Mic, Map, ChevronRight,
  CheckCircle, Clock, AlertCircle, Loader2, Gavel
} from "lucide-react";
import { toast } from "sonner";

const HERO_IMG = "https://private-us-east-1.manuscdn.com/sessionFile/hmEvCGQLHKyGnx6qwMSEHn/sandbox/qiXHjJUmj8lqJymwhLI5B2-img-1_1771695716000_na1fn_aGVyby1iYW5uZXI.png?x-oss-process=image/resize,w_1920,h_1920/format,webp/quality,q_80&Expires=1798761600&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvaG1FdkNHUUxIS3lHbng2cXdNU0VIbi9zYW5kYm94L3FpWEhqSlVtajhscUp5bXdoTEk1QjItaW1nLTFfMTc3MTY5NTcxNjAwMF9uYTFmbl9hR1Z5YnkxaVlXNXVaWEkucG5nP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLHdfMTkyMCxoXzE5MjAvZm9ybWF0LHdlYnAvcXVhbGl0eSxxXzgwIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk4NzYxNjAwfX19XX0_&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Yeq1vIhtaEw73bIbDJlFsrAQeoce-YaWvid7nAdYEKAA41Xxzh8iioV-HmHsbldg~z674zIlRc0KeBIdV2hH2O8yBRN6KjP-BMO9QHDbGeBbTw3Bd5uEbh7GmZUXb7klkd0yStYYQcIjwTPBcJ7dMkiQ4AV1k5u63gQDm1FS-hqRGqzcS97ZQc0eSd3Ij2CKLrF7OXc4Xu6wB8CxzLD87mTdnvOtLobjHgvFdl6KVkUTIHjh97fL8YRlN5My6N3BGW-E8l-ZNVnWT22qfiHcpVD4kk6S6yu~v7OpBY3-1if3am5B2prST3bHxGMKsQlTwttr~xEpX4ZYF1dAJy0n2Q__";

interface ContextPanelProps {
  selectedAgent: string | null;
  selectedTask: string | null;
}

export default function ContextPanel({ selectedAgent, selectedTask }: ContextPanelProps) {
  const agent = selectedAgent ? AGENT_CATALOG.find(a => a.id === selectedAgent) : null;
  const task = selectedTask ? MOCK_TASKS.find(t => t.id === selectedTask) : null;

  return (
    <div className="p-3 space-y-3">
      {/* Agent detail */}
      {agent && <AgentDetail agent={agent} />}

      {/* Task detail */}
      {task && <TaskDetail task={task} />}

      {/* Voice NLU */}
      <VoiceNLUPanel />

      {/* Roadmap */}
      <RoadmapPanel />
    </div>
  );
}

function AgentDetail({ agent }: { agent: Agent }) {
  return (
    <motion.div
      key={agent.id}
      initial={{ opacity: 0, x: 16 }}
      animate={{ opacity: 1, x: 0 }}
      className="panel"
    >
      <div className="panel-header flex items-center gap-2">
        <User className="w-3 h-3" />
        // AGENT DETAIL
      </div>
      <div className="p-3 space-y-3">
        <div className="flex items-center gap-2">
          <span className={`status-dot ${
            agent.status === 'active' ? 'status-dot-active' : 'status-dot-planned'
          }`} />
          <span className="text-[14px] font-semibold text-foreground">{agent.name}</span>
          <Badge variant="outline" className="text-[9px] h-4 ml-auto">
            {agent.status.toUpperCase()}
          </Badge>
        </div>

        <div className="text-[11px] text-btc-orange font-medium">{agent.role}</div>

        <p className="text-[11px] text-muted-foreground leading-relaxed">
          {agent.description}
        </p>

        <Separator className="bg-border" />

        <div className="space-y-2 text-[11px]">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Rate</span>
            {agent.rateSats === 0 ? (
              <span className="text-electric-green">FREE</span>
            ) : (
              <span className="sat-amount flex items-center gap-1">
                <Zap className="w-3 h-3" />
                {agent.rateSats} sats/task
              </span>
            )}
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Capabilities</span>
            <span className="text-foreground">{agent.capabilities.length}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-1">
          {agent.capabilities.map(cap => (
            <span key={cap} className="text-[9px] px-1.5 py-0.5 bg-accent text-accent-foreground border border-border">
              {cap}
            </span>
          ))}
        </div>

        {agent.status === 'active' && (
          <Button
            variant="ghost"
            size="sm"
            className="w-full h-7 text-[10px] text-btc-orange hover:bg-btc-orange/10 border border-btc-orange/30"
            onClick={() => toast("Chat with " + agent.name, { description: "Switch to the Chat tab to interact." })}
          >
            OPEN CHAT
            <ChevronRight className="w-3 h-3 ml-1" />
          </Button>
        )}
      </div>
    </motion.div>
  );
}

function TaskDetail({ task }: { task: Task }) {
  return (
    <motion.div
      key={task.id}
      initial={{ opacity: 0, x: 16 }}
      animate={{ opacity: 1, x: 0 }}
      className="panel"
    >
      <div className="panel-header flex items-center gap-2">
        <Clock className="w-3 h-3" />
        // TASK DETAIL
      </div>
      <div className="p-3 space-y-3">
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-muted-foreground font-mono">{task.id}</span>
          <TaskStatusBadge status={task.status} />
        </div>

        <p className="text-[12px] text-foreground leading-relaxed">
          {task.description}
        </p>

        <Separator className="bg-border" />

        <div className="space-y-2 text-[11px]">
          <div className="flex justify-between">
            <span className="text-muted-foreground">Assigned</span>
            <span className={task.assignedAgent ? 'text-btc-orange' : 'text-muted-foreground'}>
              {task.assignedAgent || 'Unassigned'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">Created</span>
            <span className="text-foreground">
              {new Date(task.createdAt).toLocaleString()}
            </span>
          </div>
          {task.completedAt && (
            <div className="flex justify-between">
              <span className="text-muted-foreground">Completed</span>
              <span className="text-electric-green">
                {new Date(task.completedAt).toLocaleString()}
              </span>
            </div>
          )}
        </div>

        {task.result && (
          <>
            <Separator className="bg-border" />
            <div>
              <div className="text-[10px] uppercase tracking-wider text-muted-foreground mb-1">Result</div>
              <p className="text-[11px] text-foreground bg-accent p-2 border border-border">
                {task.result}
              </p>
            </div>
          </>
        )}
      </div>
    </motion.div>
  );
}

function TaskStatusBadge({ status }: { status: Task["status"] }) {
  const colors: Record<Task["status"], string> = {
    pending: "bg-muted text-muted-foreground",
    bidding: "bg-warning-amber/20 text-warning-amber border-warning-amber/30",
    assigned: "bg-cyber-cyan/20 text-cyber-cyan border-cyber-cyan/30",
    running: "bg-btc-orange/20 text-btc-orange border-btc-orange/30",
    completed: "bg-electric-green/20 text-electric-green border-electric-green/30",
    failed: "bg-danger-red/20 text-danger-red border-danger-red/30",
  };
  return (
    <span className={`text-[9px] uppercase tracking-wider px-1.5 py-0.5 border ${colors[status]}`}>
      {status}
    </span>
  );
}

function VoiceNLUPanel() {
  return (
    <div className="panel">
      <div className="panel-header flex items-center gap-2">
        <Mic className="w-3 h-3" />
        // VOICE NLU
      </div>
      <div className="p-3 space-y-2">
        <p className="text-[10px] text-muted-foreground mb-2">
          Supported voice intents — local regex-based NLU, no cloud.
        </p>
        {VOICE_INTENTS.map(intent => (
          <div key={intent.name} className="flex items-start gap-2 text-[11px]">
            <span className="text-btc-orange font-medium w-14 flex-shrink-0 uppercase text-[10px]">
              {intent.name}
            </span>
            <div className="flex-1 min-w-0">
              <span className="text-muted-foreground">{intent.description}</span>
              <div className="text-[9px] text-muted-foreground/60 font-mono mt-0.5 truncate">
                "{intent.example}"
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function RoadmapPanel() {
  return (
    <div className="panel">
      <div className="panel-header flex items-center gap-2">
        <Map className="w-3 h-3" />
        // ROADMAP
      </div>
      <div className="p-3 space-y-2">
        {ROADMAP.map((item, i) => (
          <div key={item.version} className="flex items-start gap-2 text-[11px]">
            <div className="flex flex-col items-center mt-0.5">
              <span className={`w-2 h-2 rounded-full ${
                item.status === 'complete' ? 'bg-electric-green' :
                item.status === 'current' ? 'bg-btc-orange' : 'bg-muted-foreground'
              }`} />
              {i < ROADMAP.length - 1 && (
                <span className="w-px h-6 bg-border mt-1" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-foreground">{item.version}</span>
                <span className="text-btc-orange">{item.name}</span>
                {item.status === 'current' && (
                  <span className="text-[8px] px-1 py-0.5 bg-btc-orange/20 text-btc-orange border border-btc-orange/30">
                    CURRENT
                  </span>
                )}
              </div>
              <span className="text-muted-foreground text-[10px]">{item.milestone}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
