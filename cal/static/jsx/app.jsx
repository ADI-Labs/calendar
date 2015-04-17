var RApp = React.createClass({
    getInitialState: function() {
        return {eventList: [], userList: [], date: new Date()}
    },
    componentDidMount: function() {
        $.getJSON("/events/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
            this.setState({eventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
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
        $.getJSON("/events/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
            this.setState({eventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
            this.props.setState({userList: data.data});
        }.bind(this));
    },

    incrementDate: function(days) {
        var state = this.state;
        state.date.setDate(state.date.getDate() + days);
        this.setState(state);
        $.getJSON("/events/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
            this.setState({eventList: data.data});
        }.bind(this));

        $.getJSON("/users/" + this.state.date.getFullYear().toString() + "/" +
                (this.state.date.getMonth() + 1).toString() + "/" + 
                this.state.date.getDate().toString(), function(data) {
            this.props.setState({userList: data.data});
        }.bind(this));
    },

    render: function() {
        return (
            <div className="app">
                <RCalendar eventList={ this.state.eventList } 
                    incrementDate = {this.incrementDate}/>
                <RQuery eventList={this.state.eventList} 
                    userList={this.state.userList} 
                    removeUser={this.removeUser} 
                    setGlobalState={this.setState.bind(this)} 
                    setDate = {this.setDate}
                    date = {this.state.date}/>
            </div>
        );
    }
})

React.render(<RApp/>, document.getElementById("content"));
