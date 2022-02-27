
const test_container = $('.test__container');
const test_container_inner = $('.test__container__inner');
const test_container_questions = $('.test__container__question');

const question_completion_cover = $(".question__completion__cover");
const question_completion_popup = $(".question__completion__popup");
const question_complete_msg = $(".question__completion__popup__complete_msg");
const continue_button = $("[data-button-continue]");

const test_container_answers = $(".test__container__answer");
const test_btns_answer = $(".test__btns__answer");
test_btns_answer.focus();

const submit_btn = $('.test__btns__submit');
let question_num = 0;  // Determines which question the user is currently on
const data_user_answers = $("[data-user-answer]");
let users_answers = []; // Users Answers e.g. [4, 55, -12]
let data_correct = $("[data-correct]");  // Table cells to be replaced with check or cross
let questions_correct_arr = []; // Array of boolen values e.g. [true, false, true]
let questions_correct = 0;


// Timer
const test__timer = $(".test__timer");
const test__timer__ms = $(".test__timer__ms");
const startingTime = Date.now(); // An integer representing the number of milliseconds since 1970?

const startStopWatch = () => {
    let milliseconds = 0;
    let seconds = 0;
    let minutes = 0;
    let hours = 0;
    
    let oneSecond = 1000;
    let oneMinute = oneSecond * 60;
    let oneHour = oneMinute * 60;
    let oneDay = oneHour * 24;

    let timePassed = Date.now() - startingTime;

    if ( timePassed < oneSecond ) {
        milliseconds = Math.floor(timePassed / 33);
    } else if ( timePassed < oneMinute ) {
        milliseconds = Math.floor((timePassed % 1000) / 33);
        seconds = Math.floor(timePassed / 1000);
    } else if ( timePassed < oneHour ) {
        milliseconds = Math.floor((timePassed % 1000) / 33);
        seconds = Math.floor((timePassed / 1000) % 60);
        minutes = Math.floor(timePassed / 1000 / 60);
    } else if ( timePassed < oneDay ) {
        milliseconds = Math.floor((timePassed % 1000) / 33);
        seconds = Math.floor((timePassed / 1000) % 60);
        minutes = Math.floor((timePassed / 1000 / 60) % 60);
        hours = Math.floor(timePassed / 1000 / 60 / 60);
    }

    let isLessThanTen = (unit) => unit < 10 ? '0' + unit.toString() : unit;
    milliseconds = isLessThanTen(milliseconds);
    seconds = isLessThanTen(seconds);
    // console.log(seconds)
    minutes = isLessThanTen(minutes);
    hours = isLessThanTen(hours);

    let time = `${hours}:${minutes}:${seconds}.${milliseconds}`;
    // console.log('Time:', time);
    test__timer.text(time);
    return time;
}

let update = true;
setInterval(() => {
    if (update) {
        startStopWatch();
    }
}, 10);

// END of Timer

const show_continue_popup = () => {

    // If answer value is empty do not submit
    if (test_btns_answer.prop('value').length == 0) { return };

    // Disable answer input until "continue" is clicked
    test_btns_answer.prop('disabled', true);

    // Display popup
    question_completion_popup.css('opacity', 1);
    question_completion_popup.css('pointerEvents', 'all');

    // Display cover
    question_completion_cover.css('opacity', 0.5);
    question_completion_cover.css('pointerEvents', 'all');
    
    // Display completion messages
    let user_answer = test_btns_answer.prop('value').trim()
    // console.log(user_answer);
    users_answers.push(user_answer);
    let answer = test_container_answers.eq(question_num).text().trim();
    if ( user_answer == answer ) {
        question_complete_msg.css('color', '#66bb6a');
        question_complete_msg.text('CORRECT!');
        questions_correct++;
        questions_correct_arr.push(true);
    } else {
        question_complete_msg.css('color', '#ef5350');
        question_complete_msg.text('Incorrect...');
        questions_correct_arr.push(false);
    }

    question_num++;

    // Change "continue" button to say "Complete" when last question complete
    question_num === test_container_questions.length 
        ? continue_button.text('Complete')
        : null

    // Focus on "continue" button
    continue_button.focus();
}

submit_btn.on('click', e => {
    show_continue_popup();
});

test_btns_answer.on('keypress', e => e.which == 13 ? show_continue_popup() : null );


const next_question = () => {
    let num_of_test_questions = test_container_questions.length

    // Display end of test popup
    if ( question_num >= num_of_test_questions ) {
        $("[data-new-test]").on('click', e => {
            window.location.reload();
            return false;
        });

        // Change height and color
        question_completion_popup.css('height', '30rem');
        question_completion_popup.css('width', '30rem');
        question_completion_popup.css('justifyContent', 'normal');
        // question_complete_msg.css('color', '#EEE');
        question_complete_msg.css('marginTop', '0.8rem');
        continue_button.css('display', 'none');
        
        // Display Score
        question_complete_msg.text(`Score: ${questions_correct} / ${num_of_test_questions}`);

        // Display Time completed in
        $(".test__complete__time").css('display', 'block');
        update = false;
        $(".test__complete__time").text(startStopWatch());

        // Display Buttons
        $(".test__complete__btns").css('display', 'flex');
        
        // Display table (questions, answers, user_answers, correct?)
        $(".test__complete__table").css('display', 'block');
        data_user_answers.each( (index, td) => {
            $(td).text(users_answers[index]);
        });

        // Check or Cross for correct or incorrect respectively
        data_correct.each( (index, data) => {
            let isCorrect = questions_correct_arr[index]
            if ( !isCorrect ) {
                let icon = $(data).find('i')
                icon.removeClass('fa-check-circle');
                icon.addClass('fa-times-circle');
                icon.css('color', '#ef5350')
            }
        })

        $("[data-new-test]").focus();

        addResultsToHistoryForm();
        
        return
    }

    // Remove popup
    question_completion_popup.css('opacity', 0);
    question_completion_popup.css('pointerEvents', 'none');

    // Remove cover
    question_completion_cover.css('opacity', 0);
    question_completion_cover.css('pointerEvents', 'none');

    // Re-enable input and clear it
    test_btns_answer.prop('disabled', false);
    test_btns_answer.prop('value', "");

    // Shift next question into view
    let test_container_question_width = test_container_questions.outerWidth();
    let ml = test_container_inner.css('left').split('px').join('');
    ml = parseInt(ml);
    test_container_inner.css('left', ml - test_container_question_width);

    // Fade next question into view
    test_container_questions.each( (index, container) => 
        index == question_num ? $(container).css('opacity', 1) : null
    )

    // Focus on answer input
    test_btns_answer.focus();
}

continue_button.on('click', e => next_question() );

// continue_button.on('keypress', e => console.log(e.which) );
continue_button.on('keypress', e => e.which == 13 ? next_question() : null );


// sendAjax must be changed to false after ajax call to prevent next_question() method
// from being executed twice (unknown why method is being called twice)
let sendAjax = true  


const addResultsToHistoryForm = () => {

    if ( sendAjax ) {
        sendAjax = false

        let presetId = parseInt($("[data-preset-id]").data("preset-id"));
        if (isNaN(presetId)) { return };
        let score = questions_correct
        let time_completed_in = Date.now() - startingTime;

        let data = {
            "preset": presetId,
            "score": score,
            "time_completed_in": time_completed_in
        }

        $.ajax({
            url: '/history/',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken  // Accessed from base.js
            },
            method: 'POST',
            data: JSON.stringify(data),
            dataType: 'json',
            success: (data) => {
                // TODO: Remove this in production
                console.log('\n');
                // console.log(data.response)
                data.response 
                    ? console.log(data.response) 
                    : console.log('No Result....')
            }
        })
            
    }
}



