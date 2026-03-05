"use client";

export default function NeverminedBadge() {
  const agentId = process.env.NEXT_PUBLIC_NVM_AGENT_ID;

  if (!agentId) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <a
        href={`https://nevermined.app/agent/${agentId}`}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-2 px-3 py-2 text-sm text-indigo-600 bg-white border border-indigo-200 rounded-lg shadow-sm hover:bg-indigo-50 hover:border-indigo-300 transition-colors"
      >
        <span className="text-lg">⚡</span>
        <span className="font-medium">Powered by Nevermined</span>
      </a>
    </div>
  );
}
