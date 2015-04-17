var RApp = React.createClass({
    getInitialState: function() {
        return {eventList: [], userList: [], week: 0};
    },
    componentDidMount: function() {
        $.getJSON("/events/" + this.state.week.toString() , function(data) {
            this.setState({eventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + this.state.week.toString() , function(data) {
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

    setWeek: function(i) {
        var state = this.state;
        state.week = i;
        this.setState(state);
    },

    render: function() {
        return (
            <div className="app">
                <RCalendar eventList={ this.state.eventList } 
                    setGlobalState={this.setState.bind(this)} 
                    setWeek = {this.setWeek}
                    week = {this.state.week}/>
                <RQuery eventList={this.state.eventList} userList={this.state.userList} 
                        removeUser={this.removeUser} setGlobalState={this.setState.bind(this)} 
                        week={this.state.week} setWeek = {this.setWeek}/>
            </div>
        );
    }
})

React.render(<RApp/>, document.getElementById("content"));
