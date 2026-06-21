import { useEffect, useState } from "react";
import "./App.css";
import EventInput from "./components/EventInput";
import PriorityQueue from "./components/PriorityQueue";
import ClusterMap from "./components/ClusterMap";
import ClustersView from "./components/ClustersView";

type TabType = "priority" | "map" | "clusters";

function App() {
  const [clusters, setClusters] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<TabType>("priority");

  const loadPriorityQueue = async () => {
    const res = await fetch("http://localhost:8000/priority-queue");
    const data = await res.json();
    setClusters(data);
  };

  useEffect(() => {
    loadPriorityQueue();
    const interval = setInterval(loadPriorityQueue, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <section className="hero">
        <h1>🚨 Lifeline AI</h1>
        <p>
          Multi-agent emergency intelligence platform with semantic clustering,
          geocoding, and AI-powered recommendations
        </p>
      </section>

      <main className="dashboard">
        <EventInput onProcessed={loadPriorityQueue} />
        
        <div className="tabs-container">
          <div className="tabs">
            <button
              className={`tab ${activeTab === "priority" ? "active" : ""}`}
              onClick={() => setActiveTab("priority")}
            >
              📊 Priority Queue
            </button>
            <button
              className={`tab ${activeTab === "map" ? "active" : ""}`}
              onClick={() => setActiveTab("map")}
            >
              🗺️ Map View
            </button>
            <button
              className={`tab ${activeTab === "clusters" ? "active" : ""}`}
              onClick={() => setActiveTab("clusters")}
            >
              🔗 Clusters
            </button>
          </div>

          <div className="tab-content">
            {activeTab === "priority" && <PriorityQueue clusters={clusters} />}
            {activeTab === "map" && <ClusterMap clusters={clusters} />}
            {activeTab === "clusters" && <ClustersView clusters={clusters} />}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;