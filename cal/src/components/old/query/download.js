var React = require('react');


var Download = React.createClass({
  onClick: function() {
    var eids = this.props.eventList.map(function (e) {
      return e.id;
    });
    url = "/ics/?" + $.param({event_ids: eids});
        // kind of a hack, don't know how else to do it
        window.location.href = url;
      },
      render: function() {
        return (
          <button className="exportButton" onClick={ this.onClick }> Export </button>
        );
      }
    });

module.exports = Download;
