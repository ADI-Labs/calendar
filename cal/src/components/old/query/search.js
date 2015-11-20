var React = require('react');



var Download = require('./download');
var NextWeek = require('../nextweek');

var Search = React.createClass({
  

  onclick: function() {
    var url = "/events/" + toDateString(this.props.date);
    var search_string = document.getElementById("searchbar").value;
    // Empty search string check.
    var payload = search_string === "" ? {} : {search: search_string};

    $.getJSON(url, payload, function(data) {
      this.props.setGlobalState({eventList: data.data});
    }.bind(this));
  },

  onKeyPress: function(e) {
    // When user presses enter in the search bar, start a search.
    var RETURN = 13;
    if (e.charCode == RETURN) {
      this.onclick();
    }
  },

  render: function() {
    //div instead of form so that page doesn't reload
    return (
      <div className="search">
        <input id="searchbar" className="searchBar" type="text" onKeyPress={this.onKeyPress}/>
        <button onClick={this.onclick}> Search </button>
        <Download eventList={ this.props.eventList }/>
        <NextWeek incrementDate={this.props.incrementDate} />
      </div>
    );
  }
});


module.exports = Search;
