/*
 * DESIGN: "Sovereign Terminal" — Chat interface
 * Terminal-style command input with >_ prompt cursor
 * Messages displayed with typewriter aesthetic, typing indicator
 */

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Send } from "lucide-react";
import { MOCK_CHAT, type ChatMessage } from "@/lib/data";
import { motion } from "framer-motion";
import { toast } from "sonner";

export default function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>(MOCK_CHAT);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;

    // Handle slash commands
    if (input.startsWith("/")) {
      const cmd = input.slice(1).trim().split(" ")[0];
      toast(`Command recognized: /${cmd}`, {
        description: "Slash commands will be processed when connected to the backend.",
      });
      setInput("");
      return;
    }

    const userMsg: ChatMessage = {
      id: `c-${Date.now()}`,
      role: "user",
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simulate response with typing delay
    setTimeout(() => {
      setIsTyping(false);
      const assistantMsg: ChatMessage = {
        id: `c-${Date.now() + 1}`,
        role: "assistant",
        content: "I hear you, boss. Running locally on Ollama — no cloud, no telemetry. Your sovereignty is intact.\n\nThis is a demo interface. Connect me to your local Ollama instance to get real responses.\n\nSats are sovereignty, boss.",
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, assistantMsg]);
    }, 1200);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-full flex flex-col">
      {/* Messages area */}
      <div ref={scrollRef} className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: i < 4 ? i * 0.05 : 0 }}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-[80%] ${msg.role === 'system' ? 'w-full' : ''}`}>
              {/* Role label */}
              <div className={`text-[10px] uppercase tracking-[0.15em] mb-1 ${
                msg.role === 'user' ? 'text-right text-muted-foreground' :
                msg.role === 'system' ? 'text-cyber-cyan' :
                'text-btc-orange'
              }`}>
                {msg.role === 'assistant' ? '// TIMMY' :
                 msg.role === 'system' ? '// SYSTEM' :
                 '// YOU'}
              </div>

              {/* Message bubble */}
              <div className={`text-[13px] leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-accent border border-border px-4 py-3 text-foreground'
                  : msg.role === 'system'
                  ? 'bg-cyber-cyan/5 border border-cyber-cyan/20 px-4 py-3 text-cyber-cyan/80 font-mono text-[11px]'
                  : 'bg-card border border-border px-4 py-3 text-foreground'
              }`}
              style={msg.role === 'assistant' ? { borderTop: '2px solid oklch(0.75 0.18 55)' } : undefined}
              >
                {msg.content.split('\n').map((line, j) => (
                  <p key={j} className={j > 0 ? 'mt-2' : ''}>
                    {line || '\u00A0'}
                  </p>
                ))}
              </div>

              {/* Timestamp */}
              <div className={`text-[9px] text-muted-foreground mt-1 ${
                msg.role === 'user' ? 'text-right' : ''
              }`}>
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </motion.div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div>
              <div className="text-[10px] uppercase tracking-[0.15em] mb-1 text-btc-orange">
                // TIMMY
              </div>
              <div className="bg-card border border-border px-4 py-3 text-foreground"
                style={{ borderTop: '2px solid oklch(0.75 0.18 55)' }}
              >
                <div className="flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-btc-orange animate-pulse" />
                  <span className="w-1.5 h-1.5 rounded-full bg-btc-orange animate-pulse" style={{ animationDelay: '0.2s' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-btc-orange animate-pulse" style={{ animationDelay: '0.4s' }} />
                  <span className="text-[11px] text-muted-foreground ml-2">thinking...</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-border p-3">
        <div
          className="flex items-center gap-2 bg-input border border-border px-3 py-2.5 focus-within:border-btc-orange/50 transition-colors"
          onClick={() => inputRef.current?.focus()}
        >
          <span className="terminal-prompt text-[13px] select-none">&gt;_</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message or /command..."
            className="flex-1 bg-transparent text-[13px] text-foreground placeholder:text-muted-foreground outline-none"
            style={{ fontSize: '16px' }}
            disabled={isTyping}
          />
          <Button
            variant="ghost"
            size="icon"
            className="h-7 w-7 text-btc-orange hover:text-btc-orange/80 hover:bg-btc-orange/10"
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
          >
            <Send className="w-3.5 h-3.5" />
          </Button>
        </div>
        <div className="flex items-center gap-3 mt-1.5 text-[9px] text-muted-foreground">
          <span>ENTER to send</span>
          <span className="text-border">|</span>
          <span>/help for commands</span>
          <span className="text-border">|</span>
          <span className="text-electric-green/60">Local LLM — no cloud</span>
        </div>
      </div>
    </div>
  );
}
