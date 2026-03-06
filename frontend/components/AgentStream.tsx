import { useState } from 'react';

export interface AgentEvent {
  agent: string;
  status: 'running' | 'done' | 'error';
  output?: any;
}

interface AgentStreamProps {
  events: AgentEvent[];
  isRunning: boolean;
}

const agents = [
  { name: 'Scout', key: 'scout', number: '01' },
  { name: 'Brand', key: 'brand', number: '02' },
  { name: 'Builder', key: 'builder', number: '03' },
  { name: 'GTM', key: 'gtm', number: '04' },
];

export default function AgentStream({ events, isRunning }: AgentStreamProps) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const getAgentStatus = (agentKey: string) => {
    const agentEvents = events.filter(e => e.agent === agentKey);
    if (agentEvents.length === 0) return 'idle';
    return agentEvents[agentEvents.length - 1].status;
  };

  const getAgentOutput = (agentKey: string) => {
    const agentEvents = events.filter(e => e.agent === agentKey && e.status === 'done');
    return agentEvents.length > 0 ? agentEvents[0].output : null;
  };

  const toggleExpanded = (agentKey: string) => {
    setExpanded(prev => ({ ...prev, [agentKey]: !prev[agentKey] }));
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'running':
        return 'running';
      case 'done':
        return 'done';
      case 'error':
        return 'error';
      default:
        return '—';
    }
  };

  return (
    <div className="w-full max-w-[680px] mx-auto space-y-0">
      {agents.map((agent, idx) => {
        const status = getAgentStatus(agent.key);
        const output = getAgentOutput(agent.key);
        const isExpanded = expanded[agent.key];

        return (
          <div key={agent.key}>
            {idx > 0 && <div className="h-px bg-[#1a1a1a] my-6" />}
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center gap-4">
                <span 
                  className="text-[#1a1a1a]"
                  style={{ 
                    fontFamily: 'system-ui, sans-serif',
                    fontSize: '14px',
                    fontVariantNumeric: 'tabular-nums'
                  }}
                >
                  {agent.number}
                </span>
                <span 
                  className="text-[#1a1a1a]"
                  style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px' }}
                >
                  {agent.name}
                </span>
              </div>
              <span 
                className={`text-[#1a1a1a] ${status === 'running' ? 'animate-pulse' : ''}`}
                style={{ 
                  fontFamily: 'system-ui, sans-serif',
                  fontSize: '11px',
                  textTransform: 'lowercase'
                }}
              >
                {getStatusLabel(status)}
              </span>
            </div>
            
            {output && (
              <div className="mt-2 ml-[42px]">
                <button
                  onClick={() => toggleExpanded(agent.key)}
                  className="text-[#1a1a1a] underline hover:no-underline"
                  style={{ fontFamily: 'system-ui, sans-serif', fontSize: '12px' }}
                >
                  {isExpanded ? 'hide' : 'show'}
                </button>
                
                {isExpanded && (
                  <pre 
                    className="mt-2 text-[#1a1a1a] whitespace-pre-wrap"
                    style={{ fontFamily: 'monospace', fontSize: '12px', lineHeight: '1.6' }}
                  >
                    {typeof output === 'string' ? output : JSON.stringify(output, null, 2)}
                  </pre>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
