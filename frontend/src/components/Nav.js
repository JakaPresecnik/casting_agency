import { NavLink } from 'react-router-dom'

function Nav (props) {
    return (
        <nav>
            <ul>
                <NavLink to='/'><li>Home</li></NavLink>
                {props.role !== 'Unauthorized' && (
                    <NavLink to='/movies'><li>Movies</li></NavLink>
                )}
                {props.role !== 'Unauthorized' && (
                    <NavLink to='/actors'><li>Actors</li></NavLink>
                )}
            </ul>
            <div className='dropdown' >
                <p className='dropdown-pic'>{props.role}</p>
                <div className="dropdown-content">
                    <button>LOGIN</button>
                </div>
            </div>
            <div className='userboard'>
                <p>{props.role}</p> 
                {props.role === 'Unauthorized' ? (<button>LOGIN</button>) :
                <button>LOGOUT</button>}
            </div>
        </nav>
    )
}

export default Nav