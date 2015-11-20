var React = require('react');



var FilterCheckbox = require('./filtercheckbox');

var FilterForm = React.createClass({
  render: function() {
    var addFunction = this.props.addUser;
    var removeFunction = this.props.removeUser;
    var userNodes = this.props.userList.map(function(user) {
      return (
        <FilterCheckbox
          key={user.id}
          user={user} 
          removeUser={removeFunction}
          addUser={addFunction} />
      );
    });

    return (
      <div className="filterForm">
        <form action=""> 
          { userNodes }
        </form>
      </div>
      );
  }
});

module.exports = FilterForm;
