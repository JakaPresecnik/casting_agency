import { useState } from "react";
import { Link } from 'react-router-dom';

function NewActor (props) {
    const [name, setName] = useState(null);
    const [age, setAge] = useState(null);
    const [gender, setGender] = useState(null)
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = props.location.query.token
        
        try {
            const res = await fetch('/actors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    "name": name,
                    "age": age,
                    "gender": gender
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
                    <p>{data.new_actor.name} was created.</p>
                    <p>Age: {data.new_actor.age}, Gender: {data.new_actor.gender}</p>
                    <Link to='/#/actors'><button>Back to Actors</button></Link>
                </section>
            )
        }else {
            return(
                <section className='form-new'>
                    <h2>{data.error}</h2>
                    <p>{data.message}</p>
                    <Link to='/#/actors'><button>Back to actors</button></Link>
                </section>
            )
        }
    }

    return (
        <section className='form-new'>
            <h2>List a new Actor</h2>
            <form onSubmit= {e => handleSubmit(e)}>
            <label htmlFor='name'>Name:</label>
            <input onChange={e => onChangeName(e)} id='name' type='text' placeholder='Full Name' />
            <label htmlFor='age'>Age:</label>
            <input onChange={e => onChangeAge(e)} id='age' type='text' placeholder='Age' />
            <label htmlFor='gender'>Gender:</label>
            <input onChange={e => onChangeGender(e)} id='gender' type='text' placeholder='Gender' />
            <button disabled={!name || !age || !gender}>CREATE</button>
        </form>
      </section>
    )
}
export default NewActor