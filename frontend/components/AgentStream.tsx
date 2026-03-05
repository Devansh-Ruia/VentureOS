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
  { name: 'Scout', key: 'scout', icon: '🔍' },
  { name: 'Brand', key: 'brand', icon: '🏷️' },
  { name: 'Builder', key: 'builder', icon: '🏗️' },
  { name: 'GTM', key: 'gtm', icon: '📣' },
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

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'running':
        return <span className="px-2 py-1 text-xs font-medium bg-yellow-900 text-yellow-300 rounded animate-pulse">Running</span>;
      case 'done':
        return <span className="px-2 py-1 text-xs font-medium bg-green-900 text-green-300 rounded">Done</span>;
      case 'error':
        return <span className="px-2 py-1 text-xs font-medium bg-red-900 text-red-300 rounded">Error</span>;
      default:
        return <span className="px-2 py-1 text-xs font-medium bg-gray-800 text-gray-400 rounded">Idle</span>;
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-3">
      {agents.map(agent => {
        const status = getAgentStatus(agent.key);
        const output = getAgentOutput(agent.key);
        const isExpanded = expanded[agent.key];

        return (
          <div key={agent.key} className="border border-gray-800 rounded-lg p-4 bg-gray-900">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{agent.icon}</span>
                <span className="font-semibold">{agent.name}</span>
              </div>
              {getStatusBadge(status)}
            </div>
            
            {output && (
              <div className="mt-3">
                <button
                  onClick={() => toggleExpanded(agent.key)}
                  className="text-sm text-indigo-400 hover:text-indigo-300"
                >
                  {isExpanded ? '▼ Hide output' : '▶ Show output'}
                </button>
                
                {isExpanded && (
                  <div className="mt-2 p-3 bg-gray-950 rounded text-sm text-gray-300 whitespace-pre-wrap">
                    {typeof output === 'string' ? output : JSON.stringify(output, null, 2)}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
