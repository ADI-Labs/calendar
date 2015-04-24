var toDateString = function(date) {
    return (date.getFullYear().toString() + "/" +
            (date.getMonth() + 1).toString() + "/" + // +1 b/c js months start at 0
            date.getDate().toString());
};

var RApp = React.createClass({
    getInitialState: function() {
        return {eventList: [], userList: [], 
                date: new Date(), allEventList: []};
    },

    componentDidMount: function() {
        $.getJSON("/events/" + toDateString(this.state.date), function(data) {
            this.setState({eventList: data.data, allEventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + toDateString(this.state.date), function(data) {
            this.setState({userList: data.data});
        }.bind(this));
    },

    addUser: function(user_id) {
        var newEvents = this.state.allEventList.filter(function (evt) {
            return evt.user_id == user_id;
        });
        this.setState({
            eventList: this.state.eventList.concat(newEvents)
        });
    },

    removeUser: function(user_id) {
        this.setState({
            eventList:  this.state.eventList.filter(function (evt) {
                            return evt.user_id != user_id;
                        })
        });
    },

    setDate: function(date) {
        var state = this.state;
        state.date = date;
        this.setState(state);
        $.getJSON("/events/" + toDateString(this.state.date), function(data) {
            this.setState({eventList: data.data, allEventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + toDateString(this.state.date), function(data) {
            this.setState({userList: data.data});
        }.bind(this));
    },

    incrementDate: function(days) {
        var date = this.state.date;
        date.setDate(date.getDate() + days);
        this.setDate(date);
    },

    render: function() {
        return (
            <div className="app">
                <RSearch setGlobalState={this.setState.bind(this)}
                    userList={this.state.userList}
                    incrementDate={this.incrementDate}
                    date = {this.state.date}
                />
                <RCalendar eventList={ this.state.eventList } 
                    incrementDate = {this.incrementDate}
                    date = {this.state.date}/>
                <RQuery eventList={this.state.eventList} 
                    userList={this.state.userList} 
                    removeUser={this.removeUser} 
                    addUser={this.addUser}
                    setGlobalState={this.setState} 
                    date = {this.state.date}
                    setDate = {this.setDate}
                 />
            </div>
        );
    }
});

React.render(<RApp/>, document.getElementById("content"));
