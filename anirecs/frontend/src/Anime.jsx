import axios from "axios";
import React from "react";
import { toast } from "react-toastify";

const Anime = ({ title, description, tags, main_picture, rank, id, isHistory }) => {
  const watch = () => {
    const token = localStorage.getItem("token");
    axios
      .post(
        `http://localhost:8000/watch/${id}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((r) => {
        toast.success(`Anime ${title} is added to your watched list`);
      })
      .catch((e) => {
        if (e.response) {
          const status = e.response.status;
          const detail = e.response.data.detail;
          if (status === 400 && detail === "This anime is already watched by current user") {
            toast.info(`Anime "${title}" is already in your watched list.`);
          } else {
            toast.error(`Error watching anime: ${detail}`);
          }
        } else {
          toast.error("An unknown error occurred while watching the anime.");
        }
      });
  };

  return (
    <div>
      <div className="title-picture">
        <h2>{title}</h2>
        {main_picture && (
          <img
            src={main_picture}
            alt={`Main pic for ${title}`}
            className="anime-main-picture"
          />
        )}
      </div>
      <div className="anime-rank">Rank: {rank}</div>
      <p>{description}</p>
      <div className="anime-tags">
        {tags ? tags.map((t, i) => <div key={i}>{t.name}</div>) : <></>}
        {isHistory === true ? <></> : <button onClick={watch}>Watch</button>}
      </div>
    </div>
  );
};

export default Anime;
