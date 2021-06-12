import { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';

function Actors () {
    const { getAccessTokenSilently } = useAuth0();
    const [data, setData] = useState(null)

    useEffect(() => {
        (async () => {
            try {
                const token = await getAccessTokenSilently({
                    audience: 'casting_agency'
                });
                const res = await fetch('/actors', {
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
            {data.actors.map(actor => (
                <div key = {actor.id} className="movies">
                    <h3>{actor.name}</h3>
                    <p>ID: <strong>{actor.id}</strong></p>
                    <p>Age: <strong>{actor.age}</strong></p>
                    <p>Gender: <strong>{actor.gender}</strong></p>
                </div>
            ))}
        </section>
    )
}

export default Actors