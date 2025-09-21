import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { InputForm } from "@/components/InputForm";
import { BookViewer } from '@/components/BookViewer';

interface FormData {
  topic: string;
  description: string;
}

function App() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const logContainerRef = useRef<HTMLDivElement | null>(null);

  const handleGenerate = async ({ topic, description }: FormData) => {
    setIsLoading(true);
    setLogs([]);
    setTaskId(null);
    
    try {
      const response = await axios.post('http://localhost:8000/generate', { topic, description });
      setTaskId(response.data.task_id);
    } catch (error) {
      console.error("Error submitting task:", error);
      setLogs((prev) => [...prev, "Error: Could not start the task."]);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  useEffect(() => {
    if (!taskId) return;
    const eventSource = new EventSource(`http://localhost:8000/status/${taskId}`);
    
    eventSource.onmessage = (event) => {
      if (event.data === "[DONE]") {
        setIsLoading(false);
        eventSource.close();
      } else {
        setLogs((prevLogs) => [...prevLogs, event.data]);
      }
    };

    eventSource.onerror = () => {
      setIsLoading(false);
      eventSource.close();
    }

    return () => {
      eventSource.close();
    };
  }, [taskId]);

  return (
    <div className="h-screen w-screen bg-background flex">
      <div className="w-64 border-r flex-shrink-0">
        <BookViewer />
      </div>

      <div className="flex-grow flex flex-col p-4 md:p-8 min-h-0">
        <header className="text-center mb-10 flex-shrink-0">
          <h1 className="text-4xl md-text-5xl font-bold tracking-tight">
            Topic<span className="text-primary">Book</span>
          </h1>
          <p className="text-muted-foreground mt-2">
            Your personal AI-powered learning assistant.
          </p>
        </header>

        <main className="flex flex-col flex-grow min-h-0">
          <div className="flex-shrink-0">
            <InputForm onGenerate={handleGenerate} isLoading={isLoading} />
          </div>

          <div className="mt-8 flex-grow min-h-0">
            <div ref={logContainerRef} className="h-full w-full max-w-4xl mx-auto overflow-y-auto rounded-lg border bg-card p-6 font-mono text-sm">
              {logs.length === 0 && !isLoading && (
                <p className="text-muted-foreground">The log will appear here once you start a generation.</p>
              )}
              {isLoading && logs.length === 0 && (
                <p className="text-muted-foreground">Waiting for task to start...</p>
              )}
              {logs.map((log, index) => (
                <motion.p key={index} className={cn("whitespace-pre-wrap", log.startsWith('---') && "mt-4 font-bold")}>
                  {log}
                </motion.p>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App;