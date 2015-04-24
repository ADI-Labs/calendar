function formatTime(d) {
    // Remove the minutes if the time is on the hour
    var timeString = "";
    var hour = d.getHours();

    // Humanize hours.
    timeString += hour % 12 || 12;

    // Humanize minutes.
    if (d.getMinutes() !== 0) {
        timeString += ":" + d.getMinutes();
    }

    return timeString;
}

function AMPM(d) {
    // Determine whether the time is AM or PM.
    return d.getHours() < 12 ? "AM" : "PM";
}

var REvent = React.createClass({
    click: function() {
    }, 
    render: function() {
        var start = new Date(this.props.data.start);
        
        var timeString = formatTime(start);
        if (this.props.data.end !== null) {
            var end = new Date(this.props.data.end);
            var endTimeString = formatTime(end);

            // Only add start time's AM/PM if start and end dates are
            // different, or start and end are in different halves of
            // the day.
            equal_dates = start.toDateString() == end.toDateString();
            if (equal_dates || AMPM(start) != AMPM(end)) {
                timeString += AMPM(start);
            }
            timeString += " \u2013 " + formatTime(end) + AMPM(end);
        }
        else {
            timeString += AMPM(start);
        }

        return (
            <div className="event" onclick={ this.click }>
                { timeString }  <br/>
                <a href={this.props.data.url}> { this.props.data.name } </a>
            </div>
        );
    }
});

var RDay = React.createClass({
    render: function() {
        var events = this.props.eventList.map(function(evt, i) {
            return <REvent key={ evt.id } data={ evt }/>;
        });

        return (
            <td className="day">
                { events }
            </td>
        );
    }
});

var RWeek = React.createClass({
    render: function() {
        var events = [[], [], [], [], [], [], []];
        for (var i = 0; i < this.props.eventList.length; i++) {
            var evt = this.props.eventList[i];
            var start = new Date(evt.start);
            events[start.getDay()].push(evt);
        }

        var days = [];
        for (i = 0; i < 7; i++) {
            days.push( <RDay key={ i } eventList={ events[i] }/> );
        }

        return (
            <tr className="week">
                { days }
            </tr>
        );
    }
});

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
                    <RNextWeek incrementDate={this.props.incrementDate}/>
                </thead>

                <RWeek eventList={ this.props.eventList } />
            </table>
        );
    }
});

var RNextWeek = React.createClass({
    next: function() {
        this.props.incrementDate(7);
    },
    previous: function() {
        this.props.incrementDate(-7);
    },
    render: function() {
        return (
            <td> <button onClick={this.previous}> Previous Week </button> <button onClick={this.next}> Next Week </button> </td>
        );
    }
});
