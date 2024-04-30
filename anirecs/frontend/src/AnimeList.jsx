import React from 'react'
import Anime from './Anime'

const AnimeList = ({animeList}) => {
  return (
    <div className="animeList">
      {
        animeList.length>0?
          animeList.map(a => <Anime key={a.id} title={a.title} tags={a.tags} description={a.description}></Anime>)
          : 'There are no animes to show'
      }
    </div>
  )
}

export default AnimeList
