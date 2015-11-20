var React = require('react');


var Day = require('./day');


  var Week = React.createClass({
    render: function() {
      var events = [[], [], [], [], [], [], []];
      for (var i = 0; i < this.props.eventList.length; i++) {
        var evt = this.props.eventList[i];
        var start = new Date(evt.start);
        events[start.getDay()].push(evt);
      }

      var days = [];
      for (i = 0; i < 7; i++) {
        days.push( <td><Day key={ i } eventList={ events[i] }/></td> );
      }

      return (
        <tr className="week">
          { days }
        </tr>
      );
    }
  });

module.exports = Week;
