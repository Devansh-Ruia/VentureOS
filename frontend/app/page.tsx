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
              // parsing error
            }
          }
        }
      }
    } catch (error) {
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F0EDE8]">
      <nav className="border-b border-[#1a1a1a] px-8 py-6">
        <div 
          className="text-[#1a1a1a]"
          style={{ fontFamily: 'Georgia, serif', fontSize: '14px', fontWeight: '400' }}
        >
          VentureOS
        </div>
      </nav>

      <main className="max-w-[680px] mx-auto px-8 py-24">
        <div className="mb-16">
          <h1 
            className="text-[#1a1a1a] mb-6"
            style={{ 
              fontFamily: 'Georgia, serif',
              fontSize: 'clamp(40px, 6vw, 64px)',
              lineHeight: '1.05',
              textTransform: 'none'
            }}
          >
            Launch your business idea
          </h1>
          <p 
            className="text-[#555]"
            style={{ fontFamily: 'system-ui, sans-serif', fontSize: '16px', lineHeight: '1.5' }}
          >
            Four AI agents will validate, brand, build, and market your venture.
          </p>
        </div>

        <IdeaInput onSubmit={handleSubmit} disabled={isRunning} />

        {events.length > 0 && (
          <div className="mt-16">
            <AgentStream events={events} isRunning={isRunning} />
          </div>
        )}

        {brief && <VentureBrief brief={brief} />}
      </main>

      <NeverminedBadge />
    </div>
  );
}
