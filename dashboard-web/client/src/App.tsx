import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Dashboard from "./pages/Dashboard";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Dashboard} />
      <Route path="/404" component={NotFound} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="dark">
        <TooltipProvider>
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: 'oklch(0.12 0.01 260)',
                border: '1px solid oklch(0.22 0.01 260)',
                borderTop: '2px solid oklch(0.75 0.18 55)',
                color: 'oklch(0.9 0.005 90)',
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: '12px',
              },
            }}
          />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
