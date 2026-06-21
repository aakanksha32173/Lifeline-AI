import { useState } from "react";

export default function EventInput({ onProcessed }: any) {
  const [text, setText] = useState("");
  const [location, setLocation] = useState("");
  const [loading, setLoading] = useState(false);

  const submitEvent = async () => {
    if (!text.trim()) return;

    setLoading(true);

    await fetch("http://localhost:8000/events/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        source: "demo_input",
        text,
        location,
      }),
    });

    await onProcessed();

    setText("");
    setLocation("");
    setLoading(false);
  };

  return (
    <div className="card">
      <h2>Submit Crisis Report</h2>

      <div className="input-group">
        <label>Emergency report</label>
        <textarea
          placeholder="Example: My grandmother is trapped near 5th Street and needs oxygen. Water is rising quickly."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>

      <div className="input-group">
        <label>Location</label>
        <input
          placeholder="Example: Berkeley, CA"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      <button onClick={submitEvent} disabled={loading}>
        {loading ? "Processing..." : "Process Event"}
      </button>
    </div>
  );
}