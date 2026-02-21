/*
 * DESIGN: "Sovereign Terminal" — Task management panel
 * Task list with status badges, filtering, and auction indicators
 */

import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MOCK_TASKS, type Task } from "@/lib/data";
import { motion } from "framer-motion";
import { ListTodo, Plus, Filter, Clock, CheckCircle, AlertCircle, Loader2, Gavel } from "lucide-react";
import { toast } from "sonner";

interface TasksPanelProps {
  onSelectTask: (id: string) => void;
}

type StatusFilter = "all" | Task["status"];

export default function TasksPanel({ onSelectTask }: TasksPanelProps) {
  const [filter, setFilter] = useState<StatusFilter>("all");
  const [tasks] = useState<Task[]>(MOCK_TASKS);

  const filtered = filter === "all" ? tasks : tasks.filter(t => t.status === filter);

  const statusCounts = {
    all: tasks.length,
    pending: tasks.filter(t => t.status === "pending").length,
    bidding: tasks.filter(t => t.status === "bidding").length,
    assigned: tasks.filter(t => t.status === "assigned").length,
    running: tasks.filter(t => t.status === "running").length,
    completed: tasks.filter(t => t.status === "completed").length,
    failed: tasks.filter(t => t.status === "failed").length,
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header with filters */}
      <div className="border-b border-border p-3">
        <div className="flex items-center justify-between mb-3">
          <div className="text-[11px] uppercase tracking-[0.15em] text-muted-foreground flex items-center gap-2">
            <ListTodo className="w-3 h-3" />
            // TASK QUEUE
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 text-[11px] text-btc-orange hover:text-btc-orange/80 hover:bg-btc-orange/10"
            onClick={() => toast("Feature coming soon", { description: "Task creation requires backend connection." })}
          >
            <Plus className="w-3 h-3 mr-1" />
            NEW TASK
          </Button>
        </div>

        {/* Filter pills */}
        <div className="flex flex-wrap gap-1.5">
          {(["all", "pending", "bidding", "running", "completed"] as StatusFilter[]).map(s => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`text-[10px] uppercase tracking-wider px-2 py-1 transition-colors ${
                filter === s
                  ? 'bg-btc-orange/20 text-btc-orange border border-btc-orange/30'
                  : 'bg-accent text-muted-foreground border border-transparent hover:text-foreground'
              }`}
            >
              {s} ({statusCounts[s]})
            </button>
          ))}
        </div>
      </div>

      {/* Task list */}
      <ScrollArea className="flex-1">
        <div className="p-3 space-y-2">
          {filtered.map((task, i) => (
            <motion.button
              key={task.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              onClick={() => onSelectTask(task.id)}
              className="panel w-full text-left p-3 hover:bg-panel-hover transition-colors"
            >
              <div className="flex items-start gap-2">
                <StatusIcon status={task.status} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-[10px] text-muted-foreground font-mono">{task.id}</span>
                    <StatusBadge status={task.status} />
                  </div>
                  <p className="text-[12px] text-foreground leading-snug mb-1.5">
                    {task.description}
                  </p>
                  <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                    {task.assignedAgent && (
                      <span className="flex items-center gap-1">
                        → <span className="text-btc-orange">{task.assignedAgent}</span>
                      </span>
                    )}
                    <span className="flex items-center gap-1">
                      <Clock className="w-2.5 h-2.5" />
                      {new Date(task.createdAt).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            </motion.button>
          ))}

          {filtered.length === 0 && (
            <div className="text-center py-12 text-muted-foreground text-[12px]">
              No tasks matching filter "{filter}"
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}

function StatusIcon({ status }: { status: Task["status"] }) {
  const cls = "w-4 h-4 mt-0.5 flex-shrink-0";
  switch (status) {
    case "pending": return <Clock className={`${cls} text-muted-foreground`} />;
    case "bidding": return <Gavel className={`${cls} text-warning-amber`} />;
    case "assigned": return <AlertCircle className={`${cls} text-cyber-cyan`} />;
    case "running": return <Loader2 className={`${cls} text-btc-orange animate-spin`} />;
    case "completed": return <CheckCircle className={`${cls} text-electric-green`} />;
    case "failed": return <AlertCircle className={`${cls} text-danger-red`} />;
  }
}

function StatusBadge({ status }: { status: Task["status"] }) {
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
