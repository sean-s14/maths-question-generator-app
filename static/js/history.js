const time_completed_in = $("[data-time-completed-in]");

const convertTimeIntToStr = (value) => {
    let hours = 0;
    let minutes = 0;
    let seconds = 0;

    value /= 1000;

    value = value
        ? value.length == 0
            ? 0
            : value
        : 0

    if ( value > 3600 ) { // Hours
        hours = Math.floor(value / 60);
        minutes = Math.floor(value / 60);
        seconds = Math.floor(value % 60);
    } else if ( value > 60 ) { // Minutes
        minutes = Math.floor(value / 60);
        seconds = Math.floor(value % 60);
    } else { // Seconds
        seconds = value;
    }

    seconds = Math.round(seconds * 10) / 10;

    if ( hours === 0 && minutes == 0 ) {
        time = `${seconds}s`;
    } else if ( hours === 0 ) {
        time = `${minutes}m ${seconds}s`;
    } else {
        time = `${hours}h ${minutes}m ${seconds}s`;
    }

    return time;
}


time_completed_in.each( (index, time) => {
    // TODO: Modify convertTimeIntToStr function
    console.log($(time).text().trim())
    let new_time = convertTimeIntToStr($(time).text().trim());
    console.log(new_time);
    $(time).text(new_time);
})