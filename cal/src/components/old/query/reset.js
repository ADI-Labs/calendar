var React = require('react');



var Reset = React.createClass({
  onclick: function() {
        // Check all checkboxes.
        $("input[name='user'").prop('checked', true);
        this.props.setDate(new Date());
      },
      render: function() {
        return (
          <button className="reset" onClick={this.onclick}> Reset </button>
          );
      }
    });

module.exports = Reset;