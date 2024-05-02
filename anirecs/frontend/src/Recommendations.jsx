import React, { useEffect, useState } from "react";
import NavBar from "./NavBar";
import axios from "axios";
import { toast } from "react-toastify";
import AnimeList from "./AnimeList";

const Recommendations = () => {
  const [animeList, setAnimeList] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios
      .get("http://localhost:8000/recommend", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((r) => {
        setAnimeList(r.data.animes);
      })
      .catch((e) => {
        if (e.message) {
          toast.error(e.message);
        }
      });
  }, []);

  return (
    <div>
      <NavBar></NavBar>
      <AnimeList animeList={animeList}></AnimeList>
    </div>
  );
};

export default Recommendations;
