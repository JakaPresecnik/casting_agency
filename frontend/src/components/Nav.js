import { NavLink } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import LogoutButton from '../auth/LogoutButton';

function Nav () {
    const {
        user,
        isAuthenticated,
        loginWithRedirect,
      } = useAuth0();
      
    return (
        <nav>
            <ul>
                <NavLink to='/'><li>Home</li></NavLink>
                {isAuthenticated && (
                    <NavLink to='/movies'><li>Movies</li></NavLink>
                )}
                {isAuthenticated && (
                    <NavLink to='/actors'><li>Actors</li></NavLink>
                )}
            </ul>
            <div className='dropdown' >
                {isAuthenticated && <img className='dropdown-pic' src={user.picture} alt= {`Avatar of ${user.name}`} />}
                <div className="dropdown-content">
                    {!isAuthenticated ? 
                    <button onClick={() => loginWithRedirect()}>Log in</button>
                    : <LogoutButton />}
                </div>
            </div>
            <div className='userboard'>
                {isAuthenticated && <img className='dropdown-pic' src={user.picture} alt= {`Avatar of ${user.name}`} />}
                {!isAuthenticated ? <button onClick={() => loginWithRedirect()}>Log in</button>
                : <LogoutButton />}
            </div>
        </nav>
    )
}

export default Nav