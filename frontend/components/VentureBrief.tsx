interface VentureBrief {
  brand_name?: string;
  viability_score?: number;
  landing_page_url?: string;
  market_summary?: string;
  market_size?: string;
  tagline?: string;
  domain?: string;
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
  return (
    <div className="w-full max-w-[680px] mx-auto mt-16 pt-16 border-t border-[#1a1a1a]">
      <h2 
        className="text-[#1a1a1a] mb-8"
        style={{ 
          fontFamily: 'Georgia, serif',
          fontSize: 'clamp(48px, 8vw, 96px)',
          lineHeight: '0.95',
          textTransform: 'none'
        }}
      >
        {brief.brand_name || 'Untitled venture'}
      </h2>
      
      {brief.domain && (
        <p style={{
          fontSize: '13px',
          color: '#888',
          letterSpacing: '0.04em',
          marginTop: '8px',
          marginBottom: '32px'
        }}>
          {brief.domain}
        </p>
      )}
      
      {brief.viability_score !== undefined && (
        <p 
          className="text-[#1a1a1a] mb-12"
          style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px' }}
        >
          Viability score: {brief.viability_score} / 100
        </p>
      )}

      {brief.landing_page_url && (
        <div style={{ marginBottom: '48px' }}>
          <p style={{
            fontSize: '11px',
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            color: '#888',
            marginBottom: '8px'
          }}>
            Live site
          </p>
          <a
            href={brief.landing_page_url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              fontSize: '15px',
              color: '#1a1a1a',
              textDecoration: 'underline',
              textUnderlineOffset: '3px'
            }}
          >
            {brief.landing_page_url} ↗
          </a>
        </div>
      )}

      <div className="space-y-8 mb-12">
        {brief.market_summary && (
          <div>
            <h3 
              className="text-[#1a1a1a] mb-2"
              style={{ 
                fontFamily: 'system-ui, sans-serif',
                fontSize: '11px',
                letterSpacing: '0.12em',
                textTransform: 'uppercase'
              }}
            >
              Market summary
            </h3>
            <p 
              className="text-[#1a1a1a]"
              style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px', lineHeight: '1.6' }}
            >
              {brief.market_summary}
            </p>
          </div>
        )}
        
        {brief.market_size && (
          <div>
            <h3 
              className="text-[#1a1a1a] mb-2"
              style={{ 
                fontFamily: 'system-ui, sans-serif',
                fontSize: '11px',
                letterSpacing: '0.12em',
                textTransform: 'uppercase'
              }}
            >
              Market size
            </h3>
            <p 
              className="text-[#1a1a1a]"
              style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px', lineHeight: '1.6' }}
            >
              {brief.market_size}
            </p>
          </div>
        )}
        
        {brief.tagline && (
          <div>
            <h3 
              className="text-[#1a1a1a] mb-2"
              style={{ 
                fontFamily: 'system-ui, sans-serif',
                fontSize: '11px',
                letterSpacing: '0.12em',
                textTransform: 'uppercase'
              }}
            >
              Tagline
            </h3>
            <p 
              className="text-[#1a1a1a]"
              style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px', lineHeight: '1.6' }}
            >
              {brief.tagline}
            </p>
          </div>
        )}
        
        {brief.differentiation && (
          <div>
            <h3 
              className="text-[#1a1a1a] mb-2"
              style={{ 
                fontFamily: 'system-ui, sans-serif',
                fontSize: '11px',
                letterSpacing: '0.12em',
                textTransform: 'uppercase'
              }}
            >
              Differentiation
            </h3>
            <p 
              className="text-[#1a1a1a]"
              style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px', lineHeight: '1.6' }}
            >
              {brief.differentiation}
            </p>
          </div>
        )}
        
        {brief.competitors && brief.competitors.length > 0 && (
          <div>
            <h3 
              className="text-[#1a1a1a] mb-2"
              style={{ 
                fontFamily: 'system-ui, sans-serif',
                fontSize: '11px',
                letterSpacing: '0.12em',
                textTransform: 'uppercase'
              }}
            >
              Competitors
            </h3>
            <p 
              className="text-[#1a1a1a]"
              style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px' }}
            >
              {brief.competitors.join(', ')}
            </p>
          </div>
        )}
      </div>

      {brief.live_url && (
        <div className="mb-12">
          <a
            href={brief.live_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#1a1a1a] underline hover:no-underline"
            style={{ fontFamily: 'system-ui, sans-serif', fontSize: '15px' }}
          >
            view live site ↗
          </a>
        </div>
      )}

      {brief.gtm_plan && (
        <div className="space-y-8 pt-12 border-t border-[#1a1a1a]">
          <h3 
            className="text-[#1a1a1a]"
            style={{ 
              fontFamily: 'system-ui, sans-serif',
              fontSize: '11px',
              letterSpacing: '0.12em',
              textTransform: 'uppercase'
            }}
          >
            Go-to-market plan
          </h3>
          
          {brief.gtm_plan.reddit_communities && brief.gtm_plan.reddit_communities.length > 0 && (
            <div>
              <h4 
                className="text-[#1a1a1a] mb-2"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', fontWeight: '500' }}
              >
                Reddit communities
              </h4>
              <p 
                className="text-[#1a1a1a]"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', lineHeight: '1.8' }}
              >
                {brief.gtm_plan.reddit_communities.join(', ')}
              </p>
            </div>
          )}

          {brief.gtm_plan.cold_email && (
            <div>
              <h4 
                className="text-[#1a1a1a] mb-2"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', fontWeight: '500' }}
              >
                Cold email
              </h4>
              <p 
                className="text-[#1a1a1a] whitespace-pre-wrap"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', lineHeight: '1.6' }}
              >
                {brief.gtm_plan.cold_email}
              </p>
            </div>
          )}

          {brief.gtm_plan.tweet_drafts && brief.gtm_plan.tweet_drafts.length > 0 && (
            <div>
              <h4 
                className="text-[#1a1a1a] mb-2"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', fontWeight: '500' }}
              >
                Tweet drafts
              </h4>
              <div className="space-y-2">
                {brief.gtm_plan.tweet_drafts.map((tweet, i) => (
                  <p 
                    key={i}
                    className="text-[#1a1a1a]"
                    style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', lineHeight: '1.6' }}
                  >
                    — {tweet}
                  </p>
                ))}
              </div>
            </div>
          )}

          {brief.gtm_plan.product_hunt_blurb && (
            <div>
              <h4 
                className="text-[#1a1a1a] mb-2"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', fontWeight: '500' }}
              >
                Product Hunt blurb
              </h4>
              <p 
                className="text-[#1a1a1a]"
                style={{ fontFamily: 'system-ui, sans-serif', fontSize: '14px', lineHeight: '1.6' }}
              >
                {brief.gtm_plan.product_hunt_blurb}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
