import { Button } from "@/components/ui/button";
import { Terminal } from "lucide-react";
import { useLocation } from "wouter";

export default function NotFound() {
  const [, setLocation] = useLocation();

  return (
    <div className="h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-4">
        <Terminal className="w-12 h-12 text-btc-orange mx-auto" />
        <div className="text-[11px] uppercase tracking-[0.15em] text-btc-orange">
          // ERROR 404
        </div>
        <h1 className="text-[24px] font-bold text-foreground">
          Route not found
        </h1>
        <p className="text-[13px] text-muted-foreground max-w-sm mx-auto">
          The requested path does not exist in Mission Control.
          Check the URL or return to the dashboard.
        </p>
        <Button
          variant="ghost"
          className="text-[11px] text-btc-orange hover:bg-btc-orange/10 border border-btc-orange/30 mt-4"
          onClick={() => setLocation("/")}
        >
          RETURN TO MISSION CONTROL
        </Button>
      </div>
    </div>
  );
}
