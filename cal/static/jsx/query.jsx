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

