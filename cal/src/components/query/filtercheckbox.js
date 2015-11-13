var React = require('react');


var FilterCheckbox = React.createClass({

  handleChange: function(e) {
    // If user is checked, add events.
    if (e.target.checked)
      this.props.addUser(e.target.id);
    else
      this.props.removeUser(e.target.id);
  },

  render: function() {
    var user = this.props.user;
    return (
      <div className="filterForm">
        <input type="checkbox" name="user" id={user.id} onChange={this.handleChange} defaultChecked="true"/>
        <label htmlFor={user.id}>{user.name}</label>
        <br />
      </div>
    );
  },
});

module.exports = FilterCheckbox;
