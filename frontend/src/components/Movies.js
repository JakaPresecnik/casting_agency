import { useState, useEffect } from 'react';

const recieveMovies = async () => {
    const res = await fetch('/movies');
    try {
        const data = await res.json();
        return data.movies
    } catch(error) {
        console.log('Error ', error)
    }
}

const formatDate = (date) => {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday']

    const months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
        ]
    const releaseDate = new Date(date);
    const weekDay = days[releaseDate.getDay()];
    const monthDay = releaseDate.getDate();
    const month = months[releaseDate.getMonth()];
    const year = releaseDate.getFullYear();


    return `${weekDay} ${monthDay} ${month} ${year}`
}

function Movies () {
    const [data, setData] = useState([])

    useEffect(() => {
        recieveMovies()
        .then(res => setData(res))   
    }, [])


    return (
        <section>
            {data.map(movie => (
                <div key = {movie.id} className="movies">
                    <h3>{movie.title}</h3>
                    <p>ID: <strong>{movie.id}</strong></p>
                    <p>Release date: <strong>{formatDate(movie.release_date)}</strong></p>
                </div>
            ))}
        </section>
    )
}

export default Movies