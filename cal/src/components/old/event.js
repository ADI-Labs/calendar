var React = require('react');

var Event = React.createClass({
  click: function() {

  }, 
  render: function() {
    var start = new Date(this.props.data.start);
    
    var timeString = formatTime(start);
    if (this.props.data.end !== null) {
      var end = new Date(this.props.data.end);
      var endTimeString = formatTime(end);

      // \u2013 is a -
      timeString += AMPM(start) + " \u2013 " + formatTime(end) + AMPM(end);
    }
    else {
      timeString += AMPM(start);
    }

    return (
      <div className="event" onclick={ this.click }>
        <a href={this.props.data.url} target="_blank"> { this.props.data.name } </a> <br />
        { timeString }
      </div>
    );
  }
});

module.exports = Event;