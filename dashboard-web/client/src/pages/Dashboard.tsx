/*
 * DESIGN: "Sovereign Terminal" — Hacker Aesthetic with Bitcoin Soul
 * Three-column asymmetric layout:
 *   Left (narrow): Status cards — agents, health, notifications, L402
 *   Center (wide): Active workspace — Chat, Swarm, Tasks, Marketplace tabs
 *   Right (medium): Context panel — details, auctions, invoices
 */

import { useState } from "react";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { motion, AnimatePresence } from "framer-motion";
import {
  Terminal, Cpu, Zap, Bell, Shield,
  MessageSquare, Network, ListTodo, Store,
  ChevronRight, Activity, Volume2
} from "lucide-react";

import StatusSidebar from "@/components/StatusSidebar";
import ChatPanel from "@/components/ChatPanel";
import SwarmPanel from "@/components/SwarmPanel";
import TasksPanel from "@/components/TasksPanel";
import MarketplacePanel from "@/components/MarketplacePanel";
import ContextPanel from "@/components/ContextPanel";
import TopBar from "@/components/TopBar";
import { MOCK_NOTIFICATIONS } from "@/lib/data";

type TabValue = "chat" | "swarm" | "tasks" | "marketplace";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<TabValue>("chat");
  const [selectedAgent, setSelectedAgent] = useState<string | null>("timmy");
  const [selectedTask, setSelectedTask] = useState<string | null>(null);
  const [showMobileSidebar, setShowMobileSidebar] = useState(false);
  const unreadCount = MOCK_NOTIFICATIONS.filter(n => !n.read).length;

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-background">
      {/* Scanline overlay */}
      <div className="scanline-overlay" />

      {/* Top bar */}
      <TopBar
        unreadCount={unreadCount}
        onToggleSidebar={() => setShowMobileSidebar(!showMobileSidebar)}
      />

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left sidebar — status panels */}
        <aside className="hidden lg:flex w-[280px] flex-shrink-0 flex-col border-r border-border overflow-hidden">
          <ScrollArea className="flex-1">
            <StatusSidebar
              onSelectAgent={(id) => {
                setSelectedAgent(id);
                setSelectedTask(null);
              }}
              selectedAgent={selectedAgent}
            />
          </ScrollArea>
        </aside>

        {/* Mobile sidebar overlay */}
        <AnimatePresence>
          {showMobileSidebar && (
            <>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 0.5 }}
                exit={{ opacity: 0 }}
                className="lg:hidden fixed inset-0 bg-black z-40"
                onClick={() => setShowMobileSidebar(false)}
              />
              <motion.aside
                initial={{ x: -280 }}
                animate={{ x: 0 }}
                exit={{ x: -280 }}
                transition={{ type: "tween", duration: 0.2 }}
                className="lg:hidden fixed left-0 top-0 bottom-0 w-[280px] bg-background border-r border-border z-50 overflow-auto"
              >
                <div className="pt-14">
                  <StatusSidebar
                    onSelectAgent={(id) => {
                      setSelectedAgent(id);
                      setSelectedTask(null);
                      setShowMobileSidebar(false);
                    }}
                    selectedAgent={selectedAgent}
                  />
                </div>
              </motion.aside>
            </>
          )}
        </AnimatePresence>

        {/* Center workspace */}
        <main className="flex-1 flex flex-col overflow-hidden">
          <Tabs
            value={activeTab}
            onValueChange={(v) => setActiveTab(v as TabValue)}
            className="flex-1 flex flex-col overflow-hidden"
          >
            <div className="border-b border-border px-4">
              <TabsList className="bg-transparent h-10 gap-0 p-0">
                <TabsTrigger
                  value="chat"
                  className="data-[state=active]:bg-transparent data-[state=active]:text-btc-orange data-[state=active]:border-b-2 data-[state=active]:border-btc-orange rounded-none px-4 text-[11px] uppercase tracking-[0.12em] text-muted-foreground hover:text-foreground transition-colors"
                >
                  <MessageSquare className="w-3.5 h-3.5 mr-1.5" />
                  Chat
                </TabsTrigger>
                <TabsTrigger
                  value="swarm"
                  className="data-[state=active]:bg-transparent data-[state=active]:text-btc-orange data-[state=active]:border-b-2 data-[state=active]:border-btc-orange rounded-none px-4 text-[11px] uppercase tracking-[0.12em] text-muted-foreground hover:text-foreground transition-colors"
                >
                  <Network className="w-3.5 h-3.5 mr-1.5" />
                  Swarm
                </TabsTrigger>
                <TabsTrigger
                  value="tasks"
                  className="data-[state=active]:bg-transparent data-[state=active]:text-btc-orange data-[state=active]:border-b-2 data-[state=active]:border-btc-orange rounded-none px-4 text-[11px] uppercase tracking-[0.12em] text-muted-foreground hover:text-foreground transition-colors"
                >
                  <ListTodo className="w-3.5 h-3.5 mr-1.5" />
                  Tasks
                </TabsTrigger>
                <TabsTrigger
                  value="marketplace"
                  className="data-[state=active]:bg-transparent data-[state=active]:text-btc-orange data-[state=active]:border-b-2 data-[state=active]:border-btc-orange rounded-none px-4 text-[11px] uppercase tracking-[0.12em] text-muted-foreground hover:text-foreground transition-colors"
                >
                  <Store className="w-3.5 h-3.5 mr-1.5" />
                  Marketplace
                </TabsTrigger>
              </TabsList>
            </div>

            <div className="flex-1 overflow-hidden">
              <TabsContent value="chat" className="h-full m-0 p-0">
                <ChatPanel />
              </TabsContent>
              <TabsContent value="swarm" className="h-full m-0 p-0">
                <SwarmPanel
                  onSelectAgent={(id) => {
                    setSelectedAgent(id);
                    setSelectedTask(null);
                  }}
                />
              </TabsContent>
              <TabsContent value="tasks" className="h-full m-0 p-0">
                <TasksPanel
                  onSelectTask={(id) => {
                    setSelectedTask(id);
                    setSelectedAgent(null);
                  }}
                />
              </TabsContent>
              <TabsContent value="marketplace" className="h-full m-0 p-0">
                <MarketplacePanel
                  onSelectAgent={(id) => {
                    setSelectedAgent(id);
                    setSelectedTask(null);
                  }}
                />
              </TabsContent>
            </div>
          </Tabs>
        </main>

        {/* Right context panel */}
        <aside className="hidden xl:flex w-[320px] flex-shrink-0 flex-col border-l border-border overflow-hidden">
          <ScrollArea className="flex-1">
            <ContextPanel
              selectedAgent={selectedAgent}
              selectedTask={selectedTask}
            />
          </ScrollArea>
        </aside>
      </div>
    </div>
  );
}
