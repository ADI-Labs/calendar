import React from 'react';
import { Button } from 'react-bootstrap';
import moment from 'moment';

import './event.styl'


export default class Event extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      calledFB: false,
      id: '',
      date: 'No date set',
      data: {
        title: '',
        description: '',
        location: '',
        img: '',
        info: []
      }
    };
  }

  getData() {
    this.props.FB.api(
      this.props.id,
      'GET',
      {
        access_token: this.props.token,
        "fields":"name,description,start_time,end_time,place,picture.type(large)"
      },
      function(response) {
        let date = moment(response.start_time).format("dddd, MMM Do");
        let start_time = moment(response.start_time).format("h:mma");
        let end_time = response.end_time ? '-' + moment(response.end_time).format("h:mma") : '';
        this.setState({
          data: {
            title: response.name,
            description: response.description,
            img: response.picture.data.url,
            date: date,
            info: [
              date,
              start_time + end_time,
              response.place.name,
              <Button href={ 'https://www.facebook.com/' + this.props.id }>RSVP on Facebook!</Button>
            ]
          },
          calledFB: true
        });
      }.bind(this)
    );
  }

  handleClick() {
    this.props.openModal(this.state.data);
  }

  render() {
    if (Object.keys(this.props.FB).length !== 0 && !this.state.calledFB)
      this.getData();

    let date = this.state.data.date;

    let output = {}
    if (this.props.IsCarouselItem)
      output = (
        <div>
          <h3>{ this.state.data.title }</h3>
          <p><Button onClick={ this.handleClick.bind(this) }>Details</Button></p>
        </div>
      );
    else
      output = (
        <div className="event row" onClick={ this.handleClick.bind(this) } >
          <div className="col-md-6"><p><strong>{ date }</strong></p></div>
          <div className="col-md-6"><p>{ this.state.data.title }</p></div>
        </div>
      );

    return (
      <div>
        { output }
      </div>
    )
  }
}


