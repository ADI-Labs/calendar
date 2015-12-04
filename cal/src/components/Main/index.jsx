import React from 'react'
import Calendar from 'components/Calendar'
import { RouteHandler, Link } from 'react-router'
import moment from 'moment'


export default class Main extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      selected: moment(),
    };
  }


  setDate(day) {
    this.setState({ selected: day });
    this.forceUpdate();
  }


  render() {
    return (
      <div>
        <h1>Front Page!</h1>
        <Calendar
          selected={ this.state.selected }
          setDate={ this.setDate.bind(this) }
        />
        <p>{ this.state.selected.dateFormat }</p>
      </div>
    );
  }
}

