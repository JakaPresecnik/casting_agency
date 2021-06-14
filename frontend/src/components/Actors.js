import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';


function Actors () {
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

                const res = await fetch('https://jaka-casting-agency.herokuapp.com/actors?page=' + page, {
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization:`Bearer ${token}`
                    }
                });
                const resData = await res.json()
                setData(resData)
            }catch(e) {
                console.log(e)
            }
        })();
    }, [getAccessTokenSilently, deleted])

    const deleteActor = async (id) => {
        try {
            const res = await fetch('https://jaka-casting-agency.herokuapp.com/actors/' + id, {
                method: 'DELETE',
                headers: {
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
                <h1>There are no actors in the database</h1>
                <p>Please add some or contact your producer.</p>
                <Link to={{pathname: '/newactor', query: {token: token}}}><button className="new">Create new Actor</button></Link>
            </section>
        )
    }
    if(data.error) {
        return (
        <section>
            <h1>{data.error}</h1>
            <h2>{data.message}</h2>
        </section>)
    }
    return (
        <section>
            {data.actors.map(actor => (
                <div key = {actor.id} className="movies">
                    <h3>{actor.name}</h3>
                    <p>ID: <strong>{actor.id}</strong></p>
                    <p>Age: <strong>{actor.age}</strong></p>
                    <p>Gender: <strong>{actor.gender}</strong></p>
                    <Link to={{pathname: '/updateactor/' + actor.id, query: {
                            token: token,
                            id: actor.id,
                            name: actor.name,
                            age: actor.age,
                            gender: actor.gender
                        }}}><button className="update">Update</button></Link>
                    <button onClick={() => deleteActor(actor.id)} className="delete">Delete</button>
                </div>
            ))}
            <div className="pagination-menu">
                {createPagination()}
            </div>
            <Link to={{pathname: '/newactor', query: {token: token}}}><button className="new">Create new Actor</button></Link>
        </section>
    )
}

export default Actors