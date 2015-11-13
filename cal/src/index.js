// Bootstrapping module
import React from 'react'
import { render } from 'react-dom';
import Router from 'react-router';
import routes from 'routes';
//// import 'font-awesome/css/font-awesome.min.css'


Router.run(routes, Router.HistoryLocation, (Root, state) => {
  render(<Root {...state}/>, document.getElementById('content'));
});
