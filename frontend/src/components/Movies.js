import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';

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
    const [data, setData] = useState(null);
    const [token, setToken] = useState(null);
    const [deleted, setDeleted] = useState(null);
    const [page, setPage] = useState(1);

    useEffect(() => {
        (async () => {
            try {
                const token = await getAccessTokenSilently({
                    audience: 'casting_agency'
                });
                setToken(token)

                const res = await fetch('https://jaka-casting-agency.herokuapp.com/movies?page=' + page, {
                    headers: {
                        Authorization:`Bearer ${token}`
                    }
                });
                const resData = await res.json()
                setData(resData)
                console.log(resData)
            }catch(e) {
                console.log(e)
            }
        })();
    }, [getAccessTokenSilently, deleted, page])

    const deleteMovie = async (id) => {
        try {
            const res = await fetch('https://jaka-casting-agency.herokuapp.com/movies/' + id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization:`Bearer ${token}`
                }
            });
            const resData = await res.json()
            setDeleted(resData)
        }catch(e) {
            console.log(e)
        }
    }

    const selectPage = (num) => {
        setPage(num);
    }

    const createPagination = () => {
        let pageNumbers = [];
        let maxPage = Math.ceil(data.length / 3)
        for (let i = 1; i <= maxPage; i++) {
          pageNumbers.push(
            <span
              key={i}
              className={`page-num ${i === page ? 'active' : ''}`}
              onClick={() => {selectPage(i)}}>{i}
            </span>)
        }
        return pageNumbers;
      }
    
    if(deleted) {
        if(deleted.success) {
            return (
                <section>
                    <h1>Deleted!</h1>
                    <br />
                    <button onClick={(e) => setDeleted(null)} className='update'>Back</button>
                </section>
            )
        }else {
            return (<section>
                <h1>{deleted.error}</h1>
                <h2>{deleted.message}</h2>
                <button onClick={(e) => setDeleted(null)} className='update'>Back</button>
            </section>)
        }
    }

    if(!data) {
        return <section>Loading ...</section>
    }
    if(data.error && data.error === 404) {
        return (
            <section>
                <h1>There are no movies in the database</h1>
                <p>Please add some or contact your producer.</p>
                <Link to={{pathname: '/newmovie', query: {token: token}}}><button className="new">Create new Movie</button></Link>
            </section>
        )
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
                    <Link to={{pathname: '/updatemovie/' + movie.id, query: {
                            token: token,
                            id: movie.id,
                            title: movie.title,
                            releaseDate: movie.release_date
                        }}}><button className="update">Update</button></Link>
                    <button onClick={() => deleteMovie(movie.id)} className="delete">Delete</button>
                </div>
            ))}
            <div className="pagination-menu">
                {createPagination()}
            </div>
            <Link to={{pathname: '/newmovie', query: {token: token}}}><button className="new">Create new Movie</button></Link>
        </section>
    )
}

export default Movies