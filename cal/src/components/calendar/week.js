import React from 'react'

class Week extends React.Component {
  render() {
    let days = [],
        date = this.props.date,
        month = this.props.month;

    for (let i = 0; i < 7; i++) {
      let day = {
        name: date.format("dd").substring(0,1),
        number: date.date(),
        isCurrentMonth: date.month() === month.month(),
        isToday: date.isSame(new Date(), "day"),
        date: date
      };
      days.push(
        <span
          key = { day.date.toString() }
          className = {
            "day" + (day.isToday ? " today" : "")
            + (day.isCurrentMonth ? "" : " different-month")
            + (day.date.isSame(this.props.selected) ? " selected" : "") }
          onClick = { this.props.select.bind(null, day) }>

          
          {day.number}


        </span>
      );
      date = date.clone();
      date.add(1, "d");
    }

    return(
      <div className="week" keys={days[0].toString()}>
        {days}
      </div>
      );
  }
}

export default Week