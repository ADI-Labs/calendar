function formatTime(d) {
    // Remove the minutes if the time is on the hour
    var timeString = "";
    var hour = d.getHours();

    // Humanize hours.
    timeString += hour % 12 || 12;

    // Humanize minutes.
    if (d.getMinutes() < 10) {
        timeString += ":0" + d.getMinutes();
    }
    else {
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

            // \u2013 is a -
            timeString += AMPM(start) + " \u2013 " + formatTime(end) + AMPM(end);
        }
        else {
            timeString += AMPM(start);
        }

        return (
            <div className="event" onclick={ this.click }>
                <a href={this.props.data.url} target="_blank"> { this.props.data.name } </a> <br />
                { timeString }
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
                    <td> Sunday {this.getDate(0)} </td>
                    <td> Monday {this.getDate(1)} </td>
                    <td> Tuesday {this.getDate(2)} </td>
                    <td> Wednesday {this.getDate(3)} </td>
                    <td> Thursday {this.getDate(4)} </td>
                    <td> Friday {this.getDate(5)} </td>
                    <td> Saturday {this.getDate(6)} </td>
                </thead>

                <RWeek eventList={ this.props.eventList } />
            </table>
        );
    },
    getDate: function(day_of_week) {
        date = this.props.date;
        date.setDate(date.getDate() - date.getDay() + day_of_week);
        return (
            date.getMonth().toString() + "/" + date.getDate().toString()
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
            <div className="nextWeek"><button onClick={this.previous}> Previous Week </button> <button onClick={this.next}> Next Week </button></div>
        );
    }
});
