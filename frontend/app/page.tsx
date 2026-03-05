'use client';

import { useState } from 'react';
import IdeaInput from '@/components/IdeaInput';
import AgentStream, { AgentEvent } from '@/components/AgentStream';
import VentureBrief from '@/components/VentureBrief';
import NeverminedBadge from '@/components/NeverminedBadge';

interface VentureBriefData {
  brand_name: string;
  viability_score: number;
  market_summary: string;
  differentiation: string;
  competitors: string[];
  live_url: string;
  gtm_plan: {
    reddit_communities: string[];
    cold_email: string;
    tweet_drafts: string[];
    product_hunt_blurb: string;
  };
}

export default function Home() {
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [brief, setBrief] = useState<VentureBriefData | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleSubmit = async (idea: string) => {
    setEvents([]);
    setBrief(null);
    setIsRunning(true);

    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea }),
      });

      if (!response.ok || !response.body) {
        throw new Error('Failed to start stream');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6)) as AgentEvent;
              setEvents(prev => [...prev, event]);

              if (event.agent === 'orchestrator' && event.status === 'done') {
                setBrief(event.output);
                setIsRunning(false);
              }
            } catch (e) {
              console.error('Failed to parse event:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Stream error:', error);
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      <nav className="border-b border-gray-800">
        <div className="max-w-screen-xl mx-auto px-6 py-4">
          <div className="font-bold text-xl">VentureOS</div>
        </div>
      </nav>

      <main className="max-w-screen-xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4">Launch Your Business Idea</h1>
          <p className="text-xl text-gray-400">
            Four AI agents will validate, brand, build, and market your venture
          </p>
        </div>

        <IdeaInput onSubmit={handleSubmit} disabled={isRunning} />

        {events.length > 0 && (
          <div className="mt-12">
            <AgentStream events={events} isRunning={isRunning} />
          </div>
        )}

        {brief && <VentureBrief brief={brief} />}
      </main>

      <NeverminedBadge />
    </div>
  );
}
