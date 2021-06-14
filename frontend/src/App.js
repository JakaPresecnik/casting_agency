import { HashRouter, Route, Switch } from 'react-router-dom'
import { useAuth0 } from "@auth0/auth0-react";

import logo from './logo.svg';
import './App.css';
import './styles/nav.scss';
import './styles/home.scss';
import Nav from './components/Nav';
import NoMatch from './components/NoMatch';
import Home from './components/Home';
import Movies from './components/Movies';
import Actors from './components/Actors';
import NewMovie from './components/NewMovie'
import NewActor from './components/NewActor';
import UpdateActor from './components/UpdateActor';
import UpdateMovie from './components/UpdateMovie';

function App() {
  const { isLoading } = useAuth0();
  
  if(isLoading) {
    return <section>Loading ...</section>;
  }
  return (
    <HashRouter>
      <div className="App">
        <Nav />
        <Switch>
            <Route path='/' exact component={Home} />
            <Route path='/movies' exact component={Movies} />
            <Route path='/actors' component={Actors} />
            <Route path='/newmovie' component={NewMovie} />
            <Route path='/newactor' component={NewActor} />
            <Route path='/updateactor/:id' component={UpdateActor} />
            <Route path='/updatemovie/:id' component={UpdateMovie} />
            <Route component={NoMatch} />
          </Switch>
      </div>
    </HashRouter>
  );
}

export default App;
