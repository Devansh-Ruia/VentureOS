interface VentureBrief {
  brand_name?: string;
  viability_score?: number;
  market_summary?: string;
  differentiation?: string;
  competitors?: string[];
  live_url?: string;
  gtm_plan?: {
    reddit_communities?: string[];
    cold_email?: string;
    tweet_drafts?: string[];
    product_hunt_blurb?: string;
  };
}

interface VentureBriefProps {
  brief: VentureBrief;
}

export default function VentureBrief({ brief }: VentureBriefProps) {
  const getScoreColor = (score: number) => {
    if (score < 40) return 'bg-red-900 text-red-300';
    if (score < 70) return 'bg-yellow-900 text-yellow-300';
    return 'bg-green-900 text-green-300';
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-8 p-6 border border-gray-800 rounded-lg bg-gray-900">
      <h2 className="text-4xl font-bold mb-4">{brief.brand_name || 'Untitled Venture'}</h2>
      
      {brief.viability_score !== undefined && (
        <div className="mb-6">
          <span className={`px-3 py-1 text-sm font-medium rounded ${getScoreColor(brief.viability_score)}`}>
            Viability Score: {brief.viability_score}/100
          </span>
        </div>
      )}

      <div className="space-y-4 mb-6">
        {brief.market_summary && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Market Summary</h3>
            <p className="text-gray-300">{brief.market_summary}</p>
          </div>
        )}
        
        {brief.differentiation && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Differentiation</h3>
            <p className="text-gray-300">{brief.differentiation}</p>
          </div>
        )}
        
        {brief.competitors && brief.competitors.length > 0 && (
          <div>
            <h3 className="text-lg font-semibold mb-2">Competitors</h3>
            <div className="flex flex-wrap gap-2">
              {brief.competitors.map((comp, i) => (
                <span key={i} className="px-2 py-1 text-xs bg-gray-800 text-gray-300 rounded">
                  {comp}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {brief.live_url && (
        <a
          href={brief.live_url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block w-full text-center bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors mb-6"
        >
          View Live Site →
        </a>
      )}

      {brief.gtm_plan && (
        <div className="space-y-4 pt-6 border-t border-gray-800">
          <h3 className="text-xl font-semibold">Go-to-Market Plan</h3>
          
          {brief.gtm_plan.reddit_communities && brief.gtm_plan.reddit_communities.length > 0 && (
            <div>
              <h4 className="font-medium text-indigo-400 mb-1">Reddit Communities</h4>
              <ul className="list-disc list-inside text-gray-300 text-sm">
                {brief.gtm_plan.reddit_communities.map((comm, i) => (
                  <li key={i}>{comm}</li>
                ))}
              </ul>
            </div>
          )}

          {brief.gtm_plan.cold_email && (
            <div>
              <h4 className="font-medium text-indigo-400 mb-1">Cold Email</h4>
              <p className="text-gray-300 text-sm whitespace-pre-wrap">{brief.gtm_plan.cold_email}</p>
            </div>
          )}

          {brief.gtm_plan.tweet_drafts && brief.gtm_plan.tweet_drafts.length > 0 && (
            <div>
              <h4 className="font-medium text-indigo-400 mb-1">Tweet Drafts</h4>
              <ul className="list-disc list-inside text-gray-300 text-sm">
                {brief.gtm_plan.tweet_drafts.map((tweet, i) => (
                  <li key={i}>{tweet}</li>
                ))}
              </ul>
            </div>
          )}

          {brief.gtm_plan.product_hunt_blurb && (
            <div>
              <h4 className="font-medium text-indigo-400 mb-1">Product Hunt Blurb</h4>
              <p className="text-gray-300 text-sm">{brief.gtm_plan.product_hunt_blurb}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
