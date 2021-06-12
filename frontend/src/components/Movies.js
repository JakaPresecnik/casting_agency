import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

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
    const { getAccessTokenSilently } = useAuth0();
    const [data, setData] = useState(null)

    useEffect(() => {
        (async () => {
            try {
                const token = await getAccessTokenSilently({
                    audience: 'casting_agency'
                });
                const res = await fetch('/movies', {
                    headers: {
                        Authorization:`Bearer ${token}`
                    }
                })
                const resData = await res.json()
                setData(resData)
            }catch(e) {
                console.log(e)
            }
        })();
    }, [getAccessTokenSilently])

    if(!data) {
        return <section>Loading ...</section>
    }
    if(data.error) {
        return (<section>
            <h1>{data.error}</h1>
            <h2>{data.message}</h2>
        </section>)
    }

    return (
        <section>
            {data.movies.map(movie => (
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