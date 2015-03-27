var RSearch = React.createClass({
    render: function() {
        return (
            <form className="search">
                <input type="text"/>
                <input type="submit" value="Search"/>
            </form>
        );
    }
})

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

var RQuery = React.createClass({
    render: function() {
        return (
            <div className="query">
                <RSearch/>
                <RFiltering userList={ this.props.userList } removeUser={this.props.removeUser}/>
            </div>
        );
    }
})

