import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import axios from "axios";
import AnimeList from "./AnimeList";

const Home = () => {
  const [animeList, setAnimeList] = useState([]);
  const [animeTitle, setAnimeTitle] = useState("");
  const [animeDescription, setAnimeDescription] = useState("");
  const [animeGenre, setAnimeGenre] = useState("");

  useEffect(() => {
    let url = new URL("http://localhost:8000/animes");
    if (animeTitle !== "") {
      url.searchParams.append("title", animeTitle);
    }
    if (animeDescription !== "") {
      url.searchParams.append("description", animeDescription);
    }
    if (animeGenre !== "") {
      url.searchParams.append("genre", animeGenre);
    }

    axios.get(url).then((r) => {
      setAnimeList(r.data.animes);
      console.log(r);
    });
  }, [animeTitle, animeDescription, animeGenre]);

  return (
    <div>
      <NavBar></NavBar>
      <div className="search-bar">
        <div>
          <input
            value={animeTitle}
            placeholder="Anime title"
            onChange={(ev) => setAnimeTitle(ev.target.value)}
            className="search-input"
          />
          <input
            value={animeDescription}
            placeholder="Anime description"
            onChange={(ev) => setAnimeDescription(ev.target.value)}
            className="search-input"
          />
          <input
            value={animeGenre}
            placeholder="Anime genre"
            onChange={(ev) => setAnimeGenre(ev.target.value)}
            className="search-input"
          />
        </div>
      </div>
      <AnimeList animeList={animeList}></AnimeList>
    </div>
  );
};

export default Home;
