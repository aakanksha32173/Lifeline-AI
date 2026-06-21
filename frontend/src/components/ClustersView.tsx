interface Incident {
  incident_id: string;
  description: string;
  location: string;
  latitude: number | null;
  longitude: number | null;
  event_type: string;
  urgency: number;
}

interface Cluster {
  cluster_id: string;
  incidents: Incident[];
  summary: string;
  priority_score: number;
  recommended_action: string;
  cluster_color: string;
  event_category: string;
}

interface ClustersViewProps {
  clusters: Cluster[];
}

export default function ClustersView({ clusters }: ClustersViewProps) {
  const groupedClusters = clusters.reduce((acc, cluster) => {
    const category = cluster.event_category || "general";
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(cluster);
    return acc;
  }, {} as Record<string, Cluster[]>);

  const categoryNames: Record<string, string> = {
    medical: "Medical Emergencies",
    rescue: "Rescue Operations",
    environmental: "Environmental Hazards",
    infrastructure: "Infrastructure Issues",
    shelter: "Shelter & Housing",
    general: "General Alerts"
  };

  return (
    <div className="clusters-view">
      <h2>Incident Clusters by Category</h2>
      
      {Object.keys(groupedClusters).length === 0 ? (
        <div className="empty-state">
          No clusters yet. Submit crisis reports to see them grouped by category.
        </div>
      ) : (
        Object.entries(groupedClusters).map(([category, categoryClusters]) => (
          <div key={category} className="category-section">
            <h3 className="category-title">
              {categoryNames[category] || category}
              <span className="category-badge">{categoryClusters.length}</span>
            </h3>
            
            <div className="clusters-grid">
              {categoryClusters.map((cluster) => (
                <div 
                  key={cluster.cluster_id} 
                  className="cluster-card"
                  style={{ borderLeft: `4px solid ${cluster.cluster_color}` }}
                >
                  <div className="cluster-header">
                    <div 
                      className="cluster-color-indicator"
                      style={{ backgroundColor: cluster.cluster_color }}
                    ></div>
                    <div className="cluster-info">
                      <span className="cluster-id">Cluster #{cluster.cluster_id.slice(0, 8)}</span>
                      <span className="priority-badge" style={{ backgroundColor: cluster.cluster_color }}>
                        Priority: {cluster.priority_score}
                      </span>
                    </div>
                  </div>

                  <p className="cluster-summary">{cluster.summary}</p>

                  <div className="incidents-list">
                    <h4>Incidents ({cluster.incidents.length})</h4>
                    {cluster.incidents.map((incident) => (
                      <div key={incident.incident_id} className="incident-item">
                        <span className="incident-type">
                          {incident.event_type.replace(/_/g, " ")}
                        </span>
                        <span className="incident-urgency">Urgency: {incident.urgency}/10</span>
                        <p className="incident-desc">{incident.description}</p>
                        {incident.location && (
                          <p className="incident-location">📍 {incident.location}</p>
                        )}
                      </div>
                    ))}
                  </div>

                  <div className="recommendation-box">
                    <strong>Recommended Action:</strong>
                    <p>{cluster.recommended_action}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
