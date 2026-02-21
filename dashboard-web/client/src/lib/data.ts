/*
 * DESIGN: "Sovereign Terminal" — Hacker Aesthetic with Bitcoin Soul
 * Static data for the dashboard — mirrors the Python backend models
 */

export interface Agent {
  id: string;
  name: string;
  role: string;
  description: string;
  capabilities: string[];
  rateSats: number;
  status: "active" | "planned" | "offline";
}

export interface Task {
  id: string;
  description: string;
  status: "pending" | "bidding" | "assigned" | "running" | "completed" | "failed";
  assignedAgent: string | null;
  result: string | null;
  createdAt: string;
  completedAt: string | null;
}

export interface Notification {
  id: number;
  title: string;
  message: string;
  category: "swarm" | "task" | "agent" | "system" | "payment";
  timestamp: string;
  read: boolean;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
}

export interface WSEvent {
  event: string;
  data: Record<string, unknown>;
  timestamp: string;
}

// ── Agent Catalog ─────────────────────────────────────────────────────────
export const AGENT_CATALOG: Agent[] = [
  {
    id: "timmy",
    name: "Timmy",
    role: "Sovereign Commander",
    description: "Primary AI companion. Coordinates the swarm, manages tasks, and maintains sovereignty.",
    capabilities: ["chat", "reasoning", "coordination"],
    rateSats: 0,
    status: "active",
  },
  {
    id: "echo",
    name: "Echo",
    role: "Research Analyst",
    description: "Deep research and information synthesis. Reads, summarizes, and cross-references sources.",
    capabilities: ["research", "summarization", "fact-checking"],
    rateSats: 50,
    status: "planned",
  },
  {
    id: "mace",
    name: "Mace",
    role: "Security Sentinel",
    description: "Network security, threat assessment, and system hardening recommendations.",
    capabilities: ["security", "monitoring", "threat-analysis"],
    rateSats: 75,
    status: "planned",
  },
  {
    id: "helm",
    name: "Helm",
    role: "System Navigator",
    description: "Infrastructure management, deployment automation, and system configuration.",
    capabilities: ["devops", "automation", "configuration"],
    rateSats: 60,
    status: "planned",
  },
  {
    id: "seer",
    name: "Seer",
    role: "Data Oracle",
    description: "Data analysis, pattern recognition, and predictive insights from local datasets.",
    capabilities: ["analytics", "visualization", "prediction"],
    rateSats: 65,
    status: "planned",
  },
  {
    id: "forge",
    name: "Forge",
    role: "Code Smith",
    description: "Code generation, refactoring, debugging, and test writing.",
    capabilities: ["coding", "debugging", "testing"],
    rateSats: 55,
    status: "planned",
  },
  {
    id: "quill",
    name: "Quill",
    role: "Content Scribe",
    description: "Long-form writing, editing, documentation, and content creation.",
    capabilities: ["writing", "editing", "documentation"],
    rateSats: 45,
    status: "planned",
  },
];

// ── Mock Tasks ────────────────────────────────────────────────────────────
export const MOCK_TASKS: Task[] = [
  {
    id: "t-001",
    description: "Analyze Bitcoin whitepaper and summarize key innovations",
    status: "completed",
    assignedAgent: "timmy",
    result: "Summary generated: 3 key innovations identified — decentralized consensus, proof-of-work, and UTXO model.",
    createdAt: "2026-02-21T10:00:00Z",
    completedAt: "2026-02-21T10:02:30Z",
  },
  {
    id: "t-002",
    description: "Scan local network for open ports and vulnerabilities",
    status: "bidding",
    assignedAgent: null,
    result: null,
    createdAt: "2026-02-21T14:30:00Z",
    completedAt: null,
  },
  {
    id: "t-003",
    description: "Generate unit tests for the L402 proxy module",
    status: "running",
    assignedAgent: "forge",
    result: null,
    createdAt: "2026-02-21T15:00:00Z",
    completedAt: null,
  },
  {
    id: "t-004",
    description: "Write documentation for the swarm coordinator API",
    status: "pending",
    assignedAgent: null,
    result: null,
    createdAt: "2026-02-21T16:00:00Z",
    completedAt: null,
  },
  {
    id: "t-005",
    description: "Research self-custody best practices for 2026",
    status: "assigned",
    assignedAgent: "echo",
    result: null,
    createdAt: "2026-02-21T16:30:00Z",
    completedAt: null,
  },
];

// ── Mock Notifications ────────────────────────────────────────────────────
export const MOCK_NOTIFICATIONS: Notification[] = [
  {
    id: 1,
    title: "Swarm Online",
    message: "Timmy coordinator initialized. Swarm registry active.",
    category: "system",
    timestamp: "2026-02-21T10:00:00Z",
    read: true,
  },
  {
    id: 2,
    title: "Task Completed",
    message: "Bitcoin whitepaper analysis finished in 2m 30s.",
    category: "task",
    timestamp: "2026-02-21T10:02:30Z",
    read: true,
  },
  {
    id: 3,
    title: "Auction Started",
    message: "Network scan task open for bidding. 15s auction window.",
    category: "swarm",
    timestamp: "2026-02-21T14:30:00Z",
    read: false,
  },
  {
    id: 4,
    title: "Agent Assigned",
    message: "Forge won the bid for test generation at 55 sats.",
    category: "agent",
    timestamp: "2026-02-21T15:00:05Z",
    read: false,
  },
  {
    id: 5,
    title: "L402 Payment",
    message: "Invoice settled: 75 sats for Mace security scan.",
    category: "payment",
    timestamp: "2026-02-21T15:30:00Z",
    read: false,
  },
];

// ── Mock WebSocket Events ─────────────────────────────────────────────────
export const MOCK_WS_EVENTS: WSEvent[] = [
  { event: "agent_joined", data: { agent_id: "timmy", name: "Timmy" }, timestamp: "2026-02-21T10:00:00Z" },
  { event: "task_posted", data: { task_id: "t-001", description: "Analyze Bitcoin whitepaper" }, timestamp: "2026-02-21T10:00:05Z" },
  { event: "task_assigned", data: { task_id: "t-001", agent_id: "timmy" }, timestamp: "2026-02-21T10:00:10Z" },
  { event: "task_completed", data: { task_id: "t-001", agent_id: "timmy", result: "Analysis complete" }, timestamp: "2026-02-21T10:02:30Z" },
  { event: "task_posted", data: { task_id: "t-002", description: "Scan local network" }, timestamp: "2026-02-21T14:30:00Z" },
  { event: "bid_submitted", data: { task_id: "t-002", agent_id: "mace", bid_sats: 75 }, timestamp: "2026-02-21T14:30:05Z" },
  { event: "task_posted", data: { task_id: "t-003", description: "Generate unit tests" }, timestamp: "2026-02-21T15:00:00Z" },
  { event: "task_assigned", data: { task_id: "t-003", agent_id: "forge" }, timestamp: "2026-02-21T15:00:05Z" },
];

// ── Mock Chat History ─────────────────────────────────────────────────────
export const MOCK_CHAT: ChatMessage[] = [
  {
    id: "c-001",
    role: "system",
    content: "// TIMMY v1.0.0 — Sovereign Commander online\n// Ollama backend: llama3.2\n// All systems nominal. No cloud. No telemetry.",
    timestamp: "2026-02-21T10:00:00Z",
  },
  {
    id: "c-002",
    role: "user",
    content: "What is sovereignty in the context of Bitcoin?",
    timestamp: "2026-02-21T10:01:00Z",
  },
  {
    id: "c-003",
    role: "assistant",
    content: "Sovereignty in Bitcoin means self-custody — you hold your own keys, you validate your own transactions, you run your own node. No intermediary can freeze your funds, censor your payments, or inflate away your savings.\n\nThe same principle applies here: Timmy runs locally on your hardware, uses Ollama for inference, and stores everything in SQLite. No cloud dependency. No API keys to revoke. Your AI, your rules.\n\nSats are sovereignty, boss.",
    timestamp: "2026-02-21T10:01:15Z",
  },
];

// ── System Health ─────────────────────────────────────────────────────────
export interface SystemHealth {
  ollama: "up" | "down" | "unknown";
  model: string;
  swarmRegistry: "active" | "inactive";
  activeAgents: number;
  totalTasks: number;
  completedTasks: number;
  uptime: string;
  l402Balance: number;
}

export const MOCK_HEALTH: SystemHealth = {
  ollama: "up",
  model: "llama3.2",
  swarmRegistry: "active",
  activeAgents: 1,
  totalTasks: 5,
  completedTasks: 1,
  uptime: "4h 21m",
  l402Balance: 12_450,
};

// ── Voice NLU Intents ─────────────────────────────────────────────────────
export const VOICE_INTENTS = [
  { name: "chat", description: "General conversation", example: "Tell me about self-custody" },
  { name: "status", description: "System status query", example: "How are you?" },
  { name: "swarm", description: "Swarm management", example: "Spawn agent Echo" },
  { name: "task", description: "Task management", example: "Create task: scan network" },
  { name: "help", description: "List commands", example: "What can you do?" },
  { name: "voice", description: "Voice settings", example: "Speak slower" },
];

// ── Roadmap ───────────────────────────────────────────────────────────────
export const ROADMAP = [
  { version: "1.0.0", name: "Genesis", milestone: "Agno + Ollama + SQLite + Dashboard", status: "complete" as const },
  { version: "2.0.0", name: "Exodus", milestone: "MCP tools + multi-agent swarm", status: "current" as const },
  { version: "3.0.0", name: "Revelation", milestone: "Bitcoin Lightning treasury + single .app", status: "planned" as const },
];
