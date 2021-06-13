import { useState } from "react";
import { Link } from 'react-router-dom';

function NewMovie (props) {
    const [title, setTitle] = useState(null);
    const [releaseDate, setReleaseDate] = useState(null);
    const [data, setData] = useState(null)

    const onChangeTitle = e => {
        e.preventDefault();
        setTitle(e.target.value);
    }
    const onChangeDate = e => {
        e.preventDefault();
        setReleaseDate(e.target.value)
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = props.location.query.token
        
        try {
            const res = await fetch('/movies', {
                method: 'POST',
                headers: {
                    'content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    "title": title,
                    "release_date": releaseDate
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
                    <h2>Created!</h2>
                    <p>{data.new_movie.title} was created.</p>
                    <p>Relese date on: {data.new_movie.release_date}</p>
                    <Link to='/movies'><button>Back to movies</button></Link>
                </section>
            )
        }else {
            return(
                <section className='form-new'>
                    <h2>{data.error}</h2>
                    <p>{data.message}</p>
                    <Link to='/movies'><button>Back to movies</button></Link>
                </section>
            )
        }
    }

    return (
        <section className='form-new'>
            <h2>Create new Movie</h2>
            <form onSubmit= {e => handleSubmit(e)}>
            <label htmlFor='title'>Title:</label>
            <input onChange={e => onChangeTitle(e)} id='title' type='text' placeholder='Title' />
            <label htmlFor='releaseDate'>Release Date:</label>
            <input onChange={e => onChangeDate(e)} id='releaseDate' type='date' placeholder='Release Date' />
            <button disabled={!title || !releaseDate}>CREATE</button>
        </form>
      </section>
    )
}
export default NewMovie