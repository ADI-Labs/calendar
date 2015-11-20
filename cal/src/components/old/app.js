var React = require('react');
var $ = require('jquery');

var Search = require('./query/search');
var Calendar = require('./calendar');
var Query = require('./query/query');


var CalendarApp = React.createClass({

  getInitialState: function() {
    return {
      eventList: [], 
      userList: [], 
      date: new Date(), 
      allEventList: []
    };
  },

  componentDidMount: function() {
    $.getJSON("/events/" + toDateString(this.state.date), function(data) {
      this.setState({eventList: data.data, allEventList: data.data});
    }.bind(this));

    $.getJSON("/users/" + toDateString(this.state.date), function(data) {
      this.setState({userList: data.data});
    }.bind(this));
  },

  addUser: function(user_id) {
    var newEvents = this.state.allEventList.filter(function (evt) {
      return evt.user_id == user_id;
    });
    this.setState({
      eventList: this.state.eventList.concat(newEvents)
    });
  },

  removeUser: function(user_id) {
    this.setState({
      eventList: this.state.eventList.filter(function (evt) {
        return evt.user_id != user_id;
      })
    });
  },

  setDate: function(date) {
    var state = this.state;
    state.date = date;
    this.setState(state);
    $.getJSON("/events/" + toDateString(this.state.date), function(data) {
      this.setState({eventList: data.data, allEventList: data.data});
    }.bind(this));

    $.getJSON("/users/" + toDateString(this.state.date), function(data) {
      this.setState({userList: data.data});
    }.bind(this));
  },

  incrementDate: function(days) {
    var date = this.state.date;
    date.setDate(date.getDate() + days);
    this.setDate(date);
  },

  render: function() {
    return (
      <div className="app">
        <Search 
          setGlobalState={this.setState}
          eventList={this.state.eventList}
          incrementDate={this.incrementDate}
          date = {this.state.date} />
        <Calendar
          eventList={ this.state.eventList } 
          incrementDate = {this.incrementDate}
          date = {this.state.date} />
        <Query
          eventList={this.state.eventList} 
          userList={this.state.userList} 
          removeUser={this.removeUser} 
          addUser={this.addUser}
          setGlobalState={this.setState} 
          date = {this.state.date}
          setDate = {this.setDate} />
      </div>
    );
  }
});

var toDateString = function(date) {
  return (date.getFullYear().toString() + "/" 
          + (date.getMonth() + 1).toString() + "/" 
          + date.getDate().toString()); // +1 b/c js months start at 0
};



module.exports = CalendarApp;

