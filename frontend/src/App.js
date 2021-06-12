import { BrowserRouter, Route, Switch, Redirect } from 'react-router-dom'
import { useState } from 'react';

import logo from './logo.svg';
import './App.css';
import './styles/nav.scss'
import './styles/home.scss'
import Nav from './components/Nav'
import NoMatch from './components/NoMatch'
import Home from './components/Home'
import Movies from './components/Movies'
import Actors from './components/Actors'

function App() {
  const [JWT, setJWT] = useState('');
  const [role, setRole] = useState('Unauthorized')

  return (
    <BrowserRouter>
      <div className="App">
        <Nav role={role} />
        <Switch>
            <Route path='/' exact component={Home} />
            <Route path='/movies' exact component={Movies} />
            <Route path='/actors' component={Actors} />
            <Route component={NoMatch} />
          </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
