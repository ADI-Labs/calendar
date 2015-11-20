var React = require('react');




var Reset = require('./reset');
var FilterForm = require('./filterform');

var Query = React.createClass({
  render: function() {
    return (
      <div className="query">
        <Reset
          setGlobalState={this.props.setGlobalState}
          date={this.props.date}
          setDate={this.props.setDate} />
        <FilterForm
          userList={ this.props.userList }
          removeUser={this.props.removeUser}
          addUser={this.props.addUser} />
      </div>
      );
  }
});

function toDateString(date) {
  return (date.getFullYear().toString() + "/" 
            + (date.getMonth() + 1).toString() + "/" 
            + date.getDate().toString()); // +1 b/c js months start at 0
}

module.exports = Query

