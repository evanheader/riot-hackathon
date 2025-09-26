import { useEffect, useState } from "react";

function App() {
  const [recap, setRecap] = useState(null);
  const [gameName, setGameName] = useState("");
  const [tagLine, setTagLine] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchRecap = () => {
    setLoading(true);
    setRecap(null);
    const params = new URLSearchParams({ gameName, tagLine });
    fetch(
      `http://localhost:5000/recap?${params}`
    )
      .then((res) => res.json())
      .then((data) => setRecap(data))
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <h1>Rift Rewind Recap</h1>
      <div>
        <input
          type="text"
          placeholder="Riot ID (gameName)"
          value={gameName}
          onChange={(e) => setGameName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Tag Line"
          value={tagLine}
          onChange={(e) => setTagLine(e.target.value)}
        />
        <button
          onClick={fetchRecap}
          disabled={loading || !gameName || !tagLine}
        >
          {loading ? "Loading..." : "Get Recap"}
        </button>
      </div>
      {recap && (
        <div>
          <p>Games Played: {recap.games_played}</p>
          <p>Most Played Champion: {recap.most_played_champion}</p>
          <p>Winrate: {recap.winrate}</p>
          <p>Highlight: {recap.highlight}</p>
        </div>
      )}
    </div>
  );
}

export default App;
