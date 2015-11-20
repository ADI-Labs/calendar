// Bootstrapping module
import React from 'react'
import { render } from 'react-dom';
import { Router, Route, IndexRoute, Redirect } from 'react-router';
import createHistory from 'history/lib/createHashHistory'; // sketchy af
let history = createHistory({ queryKey: false });

/* Shell */
import App from 'components/App';

/* 'Pages' */
import Main from 'components/Main';
// import Event from 'components/Event';



// Routes for modals??
const INDEX = (
  <Router history={ history }>
    <Route path="/" component={ App }>
      <IndexRoute component={ Main } />
    </Route>
  </Router>
);

render(
  INDEX,
  document.getElementById('content')
);

