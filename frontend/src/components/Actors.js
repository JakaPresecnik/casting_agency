import { useState, useEffect } from 'react';

const recieveActors = async () => {
    const res = await fetch('/actors');
    try {
        const data = await res.json();
        return data.actors
    } catch(error) {
        console.log('Error ', error)
    }
}

function Actors () {
    const [data, setData] = useState([])

    useEffect(() => {
        recieveActors()
        .then(res => setData(res))   
    }, [])


    return (
        <section>
            {data.map(actor => (
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