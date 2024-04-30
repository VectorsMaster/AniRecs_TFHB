import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import axios from "axios";
import AnimeList from "./AnimeList";

const Home = () => {

  const [animeList, setAnimeList] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/animes')
      .then(r => {
        setAnimeList(r.data.animes)
        console.log(r)
    })
  },[])

  return <div>
    <NavBar></NavBar>
    <AnimeList animeList={animeList}></AnimeList>
  </div>;
};

export default Home;
