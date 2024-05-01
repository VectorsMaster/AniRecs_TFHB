import axios from "axios";
import React from "react";
import { toast } from "react-toastify";

const Anime = ({ title, description, tags, rating, id, isHistory }) => {
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
        if (e.message) {
          toast.error(e.message);
        }
      });
  };

  return (
    <div>
      <h2>{title}</h2>
      <div>{rating}</div>
      <p>{description}</p>
      <div className="anime-tags">
        {tags ? tags.map((t, i) => <div key={i}>{t.name}</div>) : <></>}
        {isHistory === true ? <></> : <button onClick={watch}>Watch</button>}
      </div>
    </div>
  );
};

export default Anime;
