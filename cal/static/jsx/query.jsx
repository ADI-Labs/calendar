var RSearch = React.createClass({
    onclick: function() {
        tag = $("input")[0]
        url = "/search/" + tag.value
        $.getJSON(url, function(data) {
            this.props.setGlobalState({eventList: data.data});
        }.bind(this));
    },
    render: function() {
        //div instead of form so that page doesn't reload
        return (
            <div className="search">
                <input type="text"/>
                <button onClick={this.onclick}> Search </button>
            </div>
        );
    }
})

var RReset = React.createClass({
    onclick: function() {
        $.getJSON('/events/', function(data) {
            this.props.setGlobalState({eventList: data.data});
        }.bind(this));

        $.getJSON('/users', function(data) {
            this.props.setGlobalState({userList: data.data});
        }.bind(this));
    },
    render: function() {
        return (
            <div className="reset">
                <button onClick={this.onclick}> Reset Events </button>
            </div>
        );
    }
})

=======
>>>>>>> Merge conflict
var RFiltering = React.createClass({
    remove: function(uid) {
        this.props.removeUser(uid)
    },

    render: function() {
        var users = [];
        for (var i = 0; i < this.props.userList.length; i++) {
            var user = this.props.userList[i];

            users.push(
                <button onClick={ this.remove.bind(this, user.id) } name={ user.id }> Remove {user.name}</button>
            );
        }

        return (
            <div className="filtering"> 
                { users }
            </div>
        );
    }
})

var RDownload = React.createClass({
    onClick: function() {
        this.props.userList
    },
    render: function() {
        return (
            <button onClick=this.onClick.bind(this)/>
        )
    }
})

var RQuery = React.createClass({
    render: function() {
        return (
            <div className="query">
                <RDownload userList={ this.props.userList }/>
                <RSearch setGlobalState={this.props.setGlobalState} />
                <RReset setGlobalState={this.props.setGlobalState} />
                <RFiltering userList={ this.props.userList } removeUser={this.props.removeUser} />
            </div>
        );
    }
})
