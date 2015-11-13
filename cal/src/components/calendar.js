var React = require('react');

var Week = require('./week');

var Calendar = React.createClass({


  getDate: function(day_of_week) {
    var date = this.props.date;
    date.setDate(date.getDate() - date.getDay() + day_of_week);
    return (date.getMonth() + 1) + "/" + date.getDate();
  },

  render: function() {
    return (
      <table className="calendar">
        <thead>
          <tr>
            <th> Sunday {this.getDate(0)} </th>
            <th> Monday {this.getDate(1)} </th>
            <th> Tuesday {this.getDate(2)} </th>
            <th> Wednesday {this.getDate(3)} </th>
            <th> Thursday {this.getDate(4)} </th>
            <th> Friday {this.getDate(5)} </th>
            <th> Saturday {this.getDate(6)} </th>
          </tr>
        </thead>
        <tbody>
          <Week eventList={ this.props.eventList } />
        </tbody>
      </table>
      );
  },

});


function formatTime(d) {
  // Remove the minutes if the time is on the hour
  var timeString = "";
  var hour = d.getHours();

  // Humanize hours.
  timeString += hour % 12 || 12;

  // Humanize minutes.
  if (d.getMinutes() < 10) {
    timeString += ":0" + d.getMinutes();
  }
  else {
    timeString += ":" + d.getMinutes();
  }

  return timeString;
}

function AMPM(d) {
  // Determine whether the time is AM or PM.
  return d.getHours() < 12 ? "AM" : "PM";
}

module.exports = Calendar;

