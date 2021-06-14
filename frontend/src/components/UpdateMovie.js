import { useState } from "react";
import { Link } from 'react-router-dom';

function UpdateMovie (props) {
    const [title, setTitle] = useState(props.location.query.title);
    const [releaseDate, setReleaseDate] = useState(props.location.query.releaseDate);
    const [data, setData] = useState(null)

    const onChangeTitle = e => {
        e.preventDefault();
        setTitle(e.target.value);
    }
    const onChangeDate = e => {
        e.preventDefault();
        setReleaseDate(e.target.value)
    }

    const handleSubmit = async (e, id) => {
        e.preventDefault();
        const token = props.location.query.token
        
        try {
            const res = await fetch('https://jaka-casting-agency.herokuapp.com/movies/' + id, {
                method: 'PATCH',
                headers: {
                    'content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    "title": title !== props.location.query.title ? title : null,
                    "release_date": releaseDate !== props.location.query.releaseDate ? releaseDate : null,
                })
            });
            const resData = await res.json()
            setData(resData)
        }catch(e) {
            console.log(e)
        }
    }

    if(data) {
        if(data.success) {
            return (
                <section className='form-new'>
                    <h2>Updated!</h2>
                    <p>{data.updated_movie.title} was updated.</p>
                    <p>Relese date on: {data.updated_movie.release_date}</p>
                    <Link to='/movies'><button>Back to Movies</button></Link>
                </section>
            )
        }else {
            return(
                <section className='form-new'>
                    <h2>{data.error}</h2>
                    <p>{data.message}</p>
                    <Link to='/movies'><button>Back to Movies</button></Link>
                </section>
            )
        }
    }

    return (
        <section className='form-new'>
            <h2>Update Movie</h2>
            <form onSubmit= {e => handleSubmit(e, props.location.query.id)}>
            <label htmlFor='title'>Title:</label>
            <input onChange={e => onChangeTitle(e)} id='title' value={title} type='text' placeholder='Title' />
            <label htmlFor='releaseDate'>Release Date:</label>
            <input onChange={e => onChangeDate(e)} id='releaseDate' value={releaseDate} type='date' placeholder='Release Date' />
            <button disabled={!title || !releaseDate}>UPDATE</button>
        </form>
      </section>
    )
}
export default UpdateMovie