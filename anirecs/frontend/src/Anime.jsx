import React from 'react'

const Anime = ({ title, description, tags, rating }) => {
  return (
    <div>
      <h2>{title}</h2>
      <div>{rating}</div>
      <p>{description}</p>
      <div className='anime-tags'>
        {
          tags ? tags.map((t, i) => <div key={i}>{t.name}</div>) : <></>
        }
      </div>
    </div>
  )
}

export default Anime
