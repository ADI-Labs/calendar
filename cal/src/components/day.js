var React = require('react');


var Event = require('./event');

  var Day = React.createClass({
    render: function() {
      var events = this.props.eventList.map(function(evt, i) {
        return <Event key={ evt.id } data={ evt } />;
      });

      return (
        <td className="day">
          { events }
        </td>
      );
    }
  });

module.exports = Day;
