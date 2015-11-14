import React from 'react'
import Calendar from './calendar/calendar'
import { RouteHandler, Link } from 'react-router'
import Moment from 'moment'

class Main extends React.Component {
  render() {

    let date = Moment.moment();
    console.log(date)
    return (
      <div>
        <h1>Example</h1>
        <Link to='example'>Go to the Example page...</Link>
        <RouteHandler />
        <Calendar selected={ date } />
      </div>
    );
  }
}

export default Main;
