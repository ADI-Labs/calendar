var RApp = React.createClass({
    getInitialState: function() {
        return {eventList: [], userList: []};
    },
    componentDidMount: function() {
        $.getJSON('/events/', function(data) {
            this.setState({eventList: data.data});
        }.bind(this));

        $.getJSON('/users', function(data) {
            this.setState({userList: data.data});
        }.bind(this));
    }, 

    removeUser: function(user_id) {
        this.setState({
            eventList:  this.state.eventList.filter(function (evt) {
                            return evt.user_id != user_id;
                        }),
            userList:   this.state.userList.filter(function (user) {
                            console.log(user.id);
                            return user.id != user_id
                        })
        });
    },

    render: function() {
        return (
            <div className="app">
                <RCalendar eventList={ this.state.eventList } />
                <RQuery eventList={this.state.eventList} userList={this.state.userList} removeUser={this.removeUser}/>
            </div>
        );
    }
})

React.render(<RApp/>, document.getElementById("content"));
