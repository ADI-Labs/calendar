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
        $("input[name='user'").prop('checked', true);
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

var RFilterCheckbox = React.createClass({
    render: function() {
        var user = this.props.user;
        return (
            <div className="filterForm">
                <input type="checkbox" name="user" id={user.id} onChange={this.handleChange} defaultChecked="true"/>
                <label for={user.id}>{user.name}</label>
                <br />
            </div>
        );
    },

    handleChange: function(e) {
        // If user is checked, add events.
        if (e.target.checked) {
            this.props.add(e.target.id);
        }
        else {
            this.props.remove(e.target.id);
        }
    }
})

var RFilterForm = React.createClass({
    remove: function(uid) {
        this.props.removeUser(uid)
    },

    add: function(uid) {
        this.props.addUser(uid)
    },

    render: function() {
        var removeFunction = this.remove;
        var addFunction = this.add;
        var userNodes = this.props.userList.map(function(user) {
            return (
                <RFilterCheckbox user={user} remove={removeFunction} add={addFunction}/>
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
})

var RDownload = React.createClass({
    onClick: function() {
        var uids = this.props.userList.map(function (user) {
            return user.id
        });
        url = "/isc/?" + $.param({event_ids: uids});
        // kind of a hack, don't know how else to do it
        window.location.href = url;
    },
    render: function() {
        return (
            <button onClick={ this.onClick.bind(this) }> Export Events </button>
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
                <RFilterForm userList={ this.props.userList } removeUser={this.props.removeUser} addUser={this.props.addUser}/>
            </div>
        );
    }
})
