export default function PriorityQueue({ clusters }: any) {
  return (
    <div className="card">
      <div className="queue-header">
        <h2>Priority Queue</h2>
        <span className="badge">{clusters.length} active</span>
      </div>

      {clusters.length === 0 ? (
        <div className="empty-state">
          No crisis reports yet. Submit a report to generate a priority queue.
        </div>
      ) : (
        clusters.map((cluster: any, index: number) => (
          <div 
            key={cluster.cluster_id} 
            className="incident-card"
            style={{ borderLeft: `5px solid ${cluster.cluster_color || '#6366f1'}` }}
          >
            <div className="incident-top">
              <div className="incident-rank">
                <span 
                  className="color-dot"
                  style={{ backgroundColor: cluster.cluster_color || '#6366f1' }}
                ></span>
                #{index + 1} Incident Cluster
              </div>
              <div 
                className="priority-score"
                style={{ backgroundColor: cluster.cluster_color || '#6366f1' }}
              >
                Score {cluster.priority_score}
              </div>
            </div>

            <div className="cluster-meta">
              <span className="event-category">
                {cluster.event_category?.toUpperCase() || 'GENERAL'}
              </span>
              <span className="incident-count">
                {cluster.incidents?.length || 1} incident(s)
              </span>
            </div>

            <p className="incident-summary">{cluster.summary}</p>

            <div className="recommendation">
              <strong>Recommended Action:</strong>{" "}
              {cluster.recommended_action}
            </div>
          </div>
        ))
      )}
    </div>
  );
}