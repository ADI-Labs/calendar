import React from 'react'
import Calendar from 'components/Calendar'
import { RouteHandler, Link } from 'react-router'
import moment from 'moment'

export default class Main extends React.Component {
  render() {

    let date = moment();

    return (
      <div>
        <h1>Front Page!</h1>
        <Calendar selected={ date } />
      </div>
    );
  }
}

