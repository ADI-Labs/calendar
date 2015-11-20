var React = require('react');

var NextWeek = React.createClass({
  next: function() {
    this.props.incrementDate(7);
  },
  previous: function() {
    this.props.incrementDate(-7);
  },
  render: function() {
    return (
      <div className="nextWeek">
        <button onClick={this.previous}> Previous Week </button>
        <button onClick={this.next}> Next Week </button>
      </div>
    );
  }
});


module.exports = NextWeek;