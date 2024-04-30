import React, { useEffect, useState } from 'react'
import NavBar from './NavBar'
import axios from 'axios';
import AnimeList from './AnimeList';
import { toast } from 'react-toastify';

const History = () => {

  const [animeList, setAnimeList] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios.get('http://localhost:8000/history', { headers: { "Authorization": `Bearer ${token}` } })
      .then(r => {
        setAnimeList(r.data.animes)
        
      })
      .catch(e => {
        if (e.message) {
          toast.error(e.message);
        }
    })
  },[])

  return (
    <div>
      <NavBar></NavBar>
      <AnimeList animeList={animeList}></AnimeList>
    </div>
  )
}

export default History
