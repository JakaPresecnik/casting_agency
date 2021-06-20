import { useState } from "react";
import { Link } from 'react-router-dom';

function UpdateActor (props) {
    const [name, setName] = useState(props.location.query.name);
    const [age, setAge] = useState(props.location.query.age);
    const [gender, setGender] = useState(props.location.query.gender)
    const [data, setData] = useState(null)

    const onChangeName = e => {
        e.preventDefault();
        setName(e.target.value);
    }
    const onChangeAge = e => {
        e.preventDefault();
        setAge(e.target.value)
    }
    const onChangeGender = e => {
        e.preventDefault();
        setGender(e.target.value);
    }

    const handleSubmit = async (e, id) => {
        e.preventDefault();
        const token = props.location.query.token
        
        try {
            const res = await fetch('/actors/' + id, {
                method: 'PATCH',
                headers: {
                    'content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    "name": name !== props.location.query.name ? name : null,
                    "age": age !== props.location.query.age ? age : null,
                    "gender": gender !== props.location.query.gender ? gender : null
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
                    <p>{data.updated_actor.name} was updated.</p>
                    <p>Age: {data.updated_actor.age}, Gender: {data.updated_actor.gender}</p>
                    <Link to='/actors'><button>Back to Actors</button></Link>
                </section>
            )
        }else {
            return(
                <section className='form-new'>
                    <h2>{data.error}</h2>
                    <p>{data.message}</p>
                    <Link to='/actors'><button>Back to actors</button></Link>
                </section>
            )
        }
    }

    return (
        <section className='form-new'>
            <h2>Update Actor</h2>
            <form onSubmit= {e => handleSubmit(e, props.location.query.id)}>
            <label htmlFor='name'>Name:</label>
            <input onChange={e => onChangeName(e)} id='name' type='text' value={name} placeholder='Full Name' />
            <label htmlFor='age'>Age:</label>
            <input onChange={e => onChangeAge(e)} id='age' type='text' value={age} placeholder='Age' />
            <label htmlFor='gender'>Gender:</label>
            <input onChange={e => onChangeGender(e)} id='gender' type='text' value={gender} placeholder='Gender' />
            <button disabled={!name || !age || !gender}>UPDATE</button>
        </form>
      </section>
    )
}
export default UpdateActor