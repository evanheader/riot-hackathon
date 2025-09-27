import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [recap, setRecap] = useState(null);
  const [gameName, setGameName] = useState("");
  const [tagLine, setTagLine] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRecap = () => {
    setLoading(true);
    setRecap(null);
    const params = new URLSearchParams({ gameName, tagLine });
    fetch(`http://localhost:5000/recap?${params}`)
      .then((res) => res.json())
      .then((data) => setRecap(data))
      .finally(() => setLoading(false));
  };

  return (
    <div className="riot-bg">
      <div className="recap-container">
        <h1 className="riot-title">Rift Rewind Recap</h1>
        <div className="input-row">
          <input
            type="text"
            placeholder="Riot ID (gameName)"
            value={gameName}
            onChange={(e) => setGameName(e.target.value)}
            className="riot-input"
          />
          <input
            type="text"
            placeholder="Tag Line"
            value={tagLine}
            onChange={(e) => setTagLine(e.target.value)}
            className="riot-input"
          />
          <button
            onClick={fetchRecap}
            disabled={loading || !gameName || !tagLine}
            className="riot-btn"
          >
            {loading ? "Loading..." : "Get Recap"}
          </button>
        </div>
        {recap && (
          <div className="recap-card">
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                marginBottom: "12px",
                justifyContent: "center",
              }}
            >
              <img
                src={recap.profile_icon_url}
                alt="Summoner Icon"
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: 12,
                  boxShadow: "0 2px 8px #000",
                }}
              />
              <span
                style={{
                  fontWeight: 700,
                  fontSize: "1.2rem",
                  color: "#f4c324ff",
                }}
              >
                {recap.summoner}
              </span>
            </div>
            <div style={{ textAlign: "left" }}>
              <p>
                <span className="recap-label">Games Played:</span>{" "}
                {recap.games_played}
              </p>
              <p style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span className="recap-label">Most Played Champion:</span>{" "}
                <img
                  src={recap.most_played_champion_img}
                  alt={recap.most_played_champion}
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: 8,
                    verticalAlign: "middle",
                    boxShadow: "0 2px 8px #000",
                  }}
                />
                {recap.most_played_champion}
              </p>
              <p>
                <span className="recap-label">Winrate:</span> {recap.winrate}
              </p>
              <p style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span className="recap-label">Highlight:</span>{" "}
                <img
                  src={recap.highlight_champion_img}
                  alt="Highlight Champion"
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: 8,
                    verticalAlign: "middle",
                    boxShadow: "0 2px 8px #000",
                  }}
                />
                {recap.highlight}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
