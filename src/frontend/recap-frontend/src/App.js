import { useEffect, useState } from "react";

function App() {
  const [recap, setRecap] = useState(null);

  useEffect(() => {
    fetch("https://12c4uiqjlj.execute-api.us-west-1.amazonaws.com/default/handler")
      .then(res => res.json())
      .then(data => setRecap(data));
  }, []);

  if (!recap) return <div>Loading...</div>;

  return (
    <div>
      <h1>Rift Rewind Recap</h1>
      <p>Games Played: {recap.games_played}</p>
      <p>Most Played Champion: {recap.most_played_champion}</p>
      <p>Winrate: {recap.winrate}</p>
      <p>Highlight: {recap.highlight}</p>
    </div>
  );
}

export default App;
