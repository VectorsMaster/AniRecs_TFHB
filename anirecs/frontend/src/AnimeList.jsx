import React from "react";
import Anime from "./Anime";

const AnimeList = ({ animeList, isHistory }) => {
  return (
    <div className="animeList">
      {animeList.length > 0
        ? animeList.map((a) => (
            <Anime
              key={a.id}
              title={a.title}
              tags={a.tags}
              description={a.description}
              id={a.id}
              isHistory={isHistory}
            ></Anime>
          ))
        : "There are no animes to show"}
    </div>
  );
};

export default AnimeList;
