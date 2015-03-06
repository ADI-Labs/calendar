function formatTime(d) {
    return d.toTimeString().slice(0, 5);
}

var REvent = React.createClass({
    click: function() {
    }, 
    render: function() {
        var start = new Date(this.props.data.start);
        var width = 1;
        var timeString = formatTime(start);
        if (this.props.data.end !== null) {
            var end = new Date(this.props.data.end);
            // TODO handle end of month problems
            width = end.getDate() - start.getDate() + 1;
            timeString += " \u2013 " + formatTime(end);
        }

        return (
            <div className="event" onclick={ this.click }>
                { timeString }  <br/>
                <a href={this.props.data.url}> { this.props.data.name } </a>
            </div>
        );
    }
})

var RDay = React.createClass({
    render: function() {
        var events = this.props.eventList.map(function(evt, i) {
            return <REvent data={ evt }/>
        });

        return (
            <td className="day">
                { events }
            </td>
        );
    }
})

var RWeek = React.createClass({
    render: function() {
        var events = [[], [], [], [], [], [], []];
        for (var i = 0; i < this.props.eventList.length; i++) {
            var evt = this.props.eventList[i];
            var start = new Date(evt.start);
            events[start.getDay()].push(evt);
        }

        var days = [];
        for (var i = 0; i < 7; i++) {
            days.push(
                <RDay eventList={ events[i] }/>
            )
        }

        return (
            <tr className="week">
                { days }
            </tr>
        );
    }
})

var RCalendar = React.createClass({
    render: function() {
        return (
            <table className="calendar">
                <thead>
                    <td> Sunday </td>
                    <td> Monday </td>
                    <td> Tuesday </td>
                    <td> Wednesday </td>
                    <td> Thursday </td>
                    <td> Friday </td>
                    <td> Saturday </td>
                </thead>

                <RWeek eventList={ this.props.eventList }/>
            </table>
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
