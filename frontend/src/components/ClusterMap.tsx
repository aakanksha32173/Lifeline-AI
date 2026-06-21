import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

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

interface ClusterMapProps {
  clusters: Cluster[];
}

function MapUpdater({ clusters }: { clusters: Cluster[] }) {
  const map = useMap();

  useEffect(() => {
    if (clusters.length > 0) {
      const validIncidents = clusters.flatMap(c => 
        c.incidents.filter(i => i.latitude && i.longitude)
      );

      if (validIncidents.length > 0) {
        const bounds = validIncidents.map(i => [i.latitude!, i.longitude!] as [number, number]);
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    }
  }, [clusters, map]);

  return null;
}

export default function ClusterMap({ clusters }: ClusterMapProps) {
  const defaultCenter: [number, number] = [37.8715, -122.2730];
  const defaultZoom = 10;

  const allIncidents = clusters.flatMap(cluster => 
    cluster.incidents.map(incident => ({
      ...incident,
      cluster_color: cluster.cluster_color,
      cluster_id: cluster.cluster_id,
      priority_score: cluster.priority_score
    }))
  );

  const validIncidents = allIncidents.filter(i => i.latitude && i.longitude);

  return (
    <div className="map-container">
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: "500px", width: "100%", borderRadius: "8px" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        <MapUpdater clusters={clusters} />

        {validIncidents.map((incident) => (
          <CircleMarker
            key={incident.incident_id}
            center={[incident.latitude!, incident.longitude!]}
            radius={8 + (incident.urgency || 0)}
            fillColor={incident.cluster_color}
            color="#fff"
            weight={2}
            opacity={1}
            fillOpacity={0.7}
          >
            <Popup>
              <div style={{ minWidth: "200px" }}>
                <h3 style={{ margin: "0 0 8px 0", fontSize: "14px", fontWeight: "bold" }}>
                  {incident.event_type.replace(/_/g, " ").toUpperCase()}
                </h3>
                <p style={{ margin: "4px 0", fontSize: "12px" }}>
                  <strong>Location:</strong> {incident.location}
                </p>
                <p style={{ margin: "4px 0", fontSize: "12px" }}>
                  <strong>Description:</strong> {incident.description}
                </p>
                <p style={{ margin: "4px 0", fontSize: "12px" }}>
                  <strong>Urgency:</strong> {incident.urgency}/10
                </p>
                <p style={{ margin: "4px 0", fontSize: "12px" }}>
                  <strong>Priority Score:</strong> {incident.priority_score}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      <div className="map-legend">
        <h4>Event Categories</h4>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#ef4444" }}></span>
          <span>Medical Emergency</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#f97316" }}></span>
          <span>Rescue Request</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#3b82f6" }}></span>
          <span>Flooding</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#eab308" }}></span>
          <span>Power Outage</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#22c55e" }}></span>
          <span>Shelter Update</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ backgroundColor: "#6366f1" }}></span>
          <span>General Alert</span>
        </div>
      </div>
    </div>
  );
}
