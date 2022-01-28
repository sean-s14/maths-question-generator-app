
const hidden = $("[data-preset-create-cover]");

hidden.on('click', e => {
    hidden.addClass('hidden');
    hidden.removeClass('cover');
    topics_choice_popup.addClass('hidden');
    timer_length_popup.addClass('hidden');
})

const topic_choice_button = $("[data-topics-choice-btn]");
const topics_choice_popup = $(".preset__field__topics__popup");

topic_choice_button.on('click', e => {
    hidden.removeClass('hidden');
    hidden.addClass('cover');
    topics_choice_popup.removeClass('hidden');
    $('#page').css('overflow', 'hidden');
})


// Select all sub-topics
const selectAllSubTopics = (topic, deselect) => {
    let subtopics = [];

    // Create subtopics list and check/uncheck checkboxes
    data_subtopics_list.find('li>label>span').each( (index, span) => {
        let input = $(span).closest('li').find('input');
        let span_subtopic = $(span).text().trim()
        let span_parent_topic = $(span).data('parent-topic').trim()
        if ( span_parent_topic === topic ) {
            subtopics.push(span_subtopic);
            deselect
                ? input.prop('checked', false)
                : input.prop('checked', true)
        }
    })

    // Select/Deselect all subtopics
    subtopics_select.find('option').each( (index, option) => {
        let option_title = $(option).text().trim()
        subtopics.includes(option_title)
            ? deselect
                ? $(option).removeAttr('selected')
                : $(option).attr('selected', true)
            : null
    })
}


const deselectTopicIfEmpty = (subtopic, parent_topic) => {
    // Loop through parent-topics and deselect topics with no selected sub-topics
    
    let subtopics = [];
    // Create array of sub-topics that have parent_topic
    data_subtopics_list.find('li>label>span').each( (index, span) => {
        let span_title = $(span).text().trim();
        let span_parent_topic = $(span).data('parent-topic');
        span_parent_topic == parent_topic
            ? subtopics.push(span_title)
            : null
    })

    let selected_subtopics = [];
    // Create array of selected sub-topics using the subtopics array
    subtopics_select.find('option').each( (index, option) => {
        let option_title = $(option).text().trim()
        subtopics.includes(option_title)
            ? $(option).prop('selected') == true
                ? selected_subtopics.push(option_title)
                : null
            : null
    })

    // Deselect topic
    if ( selected_subtopics.length == 0 ) {
        topics_select.find('option').each( (index, option) => {
            let option_title = $(option).text().trim();
            option_title == parent_topic
                ? $(option).removeAttr('selected')
                : null 
        })
        data_topics_list.find('li>div').each( (index, div) => {
            let span_title = $(div).find('label>span').text().trim();
            let input = $(div).find('input');

            span_title == parent_topic
                ? input.prop('checked', false)
                : null
        })
    }
}


// Topics & Sub-topics Selection
const eventSelectOption = (label, isTopic) => {
    $(label).on('click', e => {
        let title = $(label).find('span').text().trim();
        let select_input = isTopic ? topics_select : subtopics_select
        let select_options = select_input.find('option');
        select_options.each( (index, option) => {
            let option_title = $(option).text().trim();
            // If text of label clicked on is equal to the option's title 
            // then set selected to true
            
            if ( title === option_title ) {
                if ( $(option).prop('selected') == true ) {
                    $(option).removeAttr('selected')
                    selectAllSubTopics(title, deselect=true);
                } else {
                    $(option).attr('selected', true)
                    selectAllSubTopics(title);
                }
            }
        })
        
        if ( !isTopic ) {
            // If sub-topic then loop through topics and if topic.title matches 
            // subtopic.parent_topic then set corresponding topic option to selected
            let parent_topic = $(label).find('span').data('parent-topic');
            topics_select.find('option').each( (index, topicOption) => {
                let topic_option_title = $(topicOption).text().trim();
                if ( parent_topic === topic_option_title ) {
                    // Set topic option to "selected" and corresponding checkbox to true
                    $(topicOption).attr('selected', true);
                    data_topics_list.each( (index, list) => {
                        let topic_labels = $(list).find('li>div>label');
                        topic_labels.each( (index, label) => {
                            let topic_span = $(label).find('span').text().trim()
                            let input = $(label).closest('div').find('input');
                            parent_topic === topic_span
                                ?  input.prop('checked', true)
                                : null
                        })
                    })
                }
            })
            // Loop through parent-topics and deselect topics with no selected sub-topics
            deselectTopicIfEmpty(title, parent_topic);
        }
    })
}

// Topics
const topics_select = $("#id_topics");
const data_topics_list = $(".preset__field__topics__popup");

data_topics_list.each( (index, ul) => {
    let topic_labels = $(ul).find('li>div>label');
    topic_labels.each( (index, label) => {
        eventSelectOption(label, true);
    })
})

// Sub Topics
const subtopics_select = $("#id_sub_topics");
const data_subtopics_list = $("[data-subtopics-list]");
const data_subtopics_toggle = $("[data-subtopics-toggle]");

data_subtopics_list.each( (index, ul) => {
    $(ul).hide()
    let subtopic_labels = $(ul).find('li>label');
    subtopic_labels.each( (index, label) => {
        eventSelectOption(label);
    })
})

// Toggle Sub Topics
data_subtopics_toggle.each( (index, toggler) => {
    $(toggler).on('click', e => {
        data_subtopics_list.eq(index).toggle('400');
        let icon = $(toggler).find('i');
        if ( icon.css('transform') == 'matrix(-1, 1.22465e-16, -1.22465e-16, -1, 0, 0)') {
            icon.css('transform', 'rotate(90deg)');
        } else {
            icon.css('transform', 'rotate(180deg)');
        }
    })
})


// Timer
const hidden_timer_select_field = $("#id_timer");
const hidden_timer_select_options = hidden_timer_select_field.find('option');

const timer_checkbox_label = $('[for="id_timer_checkbox"]');
const timer_checkbox_input = $("#id_timer_checkbox");

const timer_type_field = $("[data-timer-type-field]");
const timer_length_field = $("[data-timer-length-field]");

const timer_type_select = $("#id_timer_type");
const timer_type_radio = $('[name="custom_timer_type"]'); // List of 2 radios




let message_error = $(".message__error")
message_error.on('click', e => {
    message_error.css('opacity', 0);
    setTimeout(() => {
        message_error.remove();
    }, 500);
})

const setTimerTypeDefault = () => {
    timer_type_select.find('option').each( (index, option) => {
        let option_value = $(option).prop('value');
        $(option).removeAttr('selected');
        option_value == 'SW'
            ? $(option).attr('selected', true)
            : null
    })
}

const isCountdown = () => {
    timer_type_select.find('option').each( (index, option) => {
        let option_value = $(option).prop('value');
        let isSelected = $(option).prop('selected');

        option_value == 'CD' && isSelected
            ? timer_length_field.css('display', 'flex')
            : timer_length_field.css('display', 'none')
    })
}

const hideOrShowTimerTypeField = () => {
    let value = timer_checkbox_input.prop('checked');
    // Hide/Show timer-type-field
    if ( value ) {
        timer_type_field.css('display', 'flex');
        // timer_length_field.css('display', 'flex');
        hidden_timer_select_options.each( (index, option) => {
            // Add attribute if true otherwise remove attribute
            value
                ? $(option).text().trim() == 'Yes'
                    ? $(option).attr('selected', true)
                    : $(option).removeAttr('selected')
                : $(option).text().trim() == 'No'
                    ? $(option).attr('selected', true)
                    : $(option).removeAttr('selected')
        })
    } else {
        timer_type_field.css('display', 'none');
        timer_length_field.css('display', 'none');
    }
}

const hideOrShowTimerCountdownField = () => {
    timer_type_radio.each( (index, input) => {
        let isChecked = $(input).prop('checked');
        let input_id = $(input).prop('id');

        timer_type_select.find('option').each( (index, option) => {
            let option_value = $(option).prop('value');

            (option_value == 'SW') && (input_id == 'timer_type_stopwatch') && isChecked
                ? $(option).attr('selected', true)
                : option_value == 'CD' && input_id == 'timer_type_countdown' && isChecked
                    ? $(option).attr('selected', true)
                    : null

            isCountdown();
        })
    })
}

// Toggle checkbox and hidden select field
timer_checkbox_label.on('click', e => {
    let value = timer_checkbox_input.prop('checked');
    
    // Change checkbox value
    value
        ? timer_checkbox_input.attr('checked', false)
        : timer_checkbox_input.attr('checked', true);
    
    // Reassign value
    value = timer_checkbox_input.prop('checked');

    // Change select value
    hidden_timer_select_options.each( (index, option) => {
        // Add attribute if true otherwise remove attribute
        value
            ? $(option).text().trim() == 'Yes'
                ? $(option).attr('selected', true)
                : $(option).removeAttr('selected')
            : $(option).text().trim() == 'No'
                ? $(option).attr('selected', true)
                : $(option).removeAttr('selected')     
    })
    
    hideOrShowTimerTypeField();

    return false
})

timer_type_radio.each( (index, input) => {
    $(input).on('click', e => {
        let isChecked = $(input).prop('checked');
        let input_id = $(input).prop('id')

        timer_type_select.find('option').each( (index, option) => {
            let option_value = $(option).prop('value');

            $(option).removeAttr('selected');

            option_value == 'SW' && input_id == 'timer_type_stopwatch'
                ? $(option).attr('selected', true)
                : null

            option_value == 'CD' && input_id == 'timer_type_countdown'
                ? $(option).attr('selected', true)
                : null

            // Conditionally display timer length button for popup
            isCountdown();
        })
    })
})

const timer_length_popup = $(".preset__field__timer__length__popup");
const timer_length_button = $(".preset__field__timer__length");

timer_length_button.on('click', e => {
    hidden.removeClass('hidden');
    hidden.addClass('cover');
    timer_length_popup.removeClass('hidden');
    $('#page').css('overflow', 'hidden');
})

const timer_length_increase_btns = $("[data-timer-length-increase-btns]");
const timer_length_decrease_btns = $("[data-timer-length-decrease-btns]");
const timer_length_popup_inputs = $(".preset__field__timer__length__popup__inputs");

// Input to be submitted
const id_timer_length_field = $("#id_timer_length");

const isLessThan10 = (value) => {
    value = parseInt(value);
    value = value < 10
        ? '0' + value.toString()
        : value
    
    value = value.toString();
    return value
}


const convertTimeStrToInt = (hours, minutes, seconds) => {
    let time = 0;

    seconds = parseInt(seconds)
    minutes = parseInt(minutes) * 60
    hours   = parseInt(hours)   * 60 * 60

    time = hours + minutes + seconds
    return time
}

// For edit page
const convertTimeIntToStr = (value) => {
    let hours = '00';
    let minutes = '00';
    let seconds = '00';

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

    hours = isLessThan10(hours)
    minutes = isLessThan10(minutes)
    seconds = isLessThan10(seconds)

    return [hours, minutes, seconds]
}

const incrementTime = (unit, decrement=false) => {
    let time = 0;

    // Set current time for particular unit
    timer_length_button.find('.btn.btn--outline').find('span').each( (index, span) => {
        let span_unit = $(span).data('span-timer-unit').trim();
        let span_value = $(span).text().trim();
        time = unit == span_unit ? span_value : time;
    })

    unit == 'hours'
        ? decrement
            ? time <= 0
                ? time = 23
                : time--
            : time >= 23
                ? time = 0
                : time++
        : decrement
            ? time <= 0
                ? time = 59
                : time--
            : time >= 59
                ? time = 0
                : time++

    time = time.toString();
    time = isLessThan10(time)

    timer_length_button.find('.btn.btn--outline').find('span').each( (index, span) => {
        let span_unit = $(span).data('span-timer-unit').trim();
        let span_value = $(span).text().trim();

        unit == span_unit
            ? $(span).text(time)
            : null
    })

    timer_length_popup_inputs.find('input').each( (index, input) => {
        let input_unit = $(input).data('timer-length-input').trim();
        let input_value = $(input).prop('value');
        unit == input_unit
            ? $(input).prop('value', time)
            : null
    })


    let hours = 0;
    let minutes = 0;
    let seconds = 0;

    timer_length_popup_inputs.find('input').each( (index, input) => {
        let input_unit = $(input).data('timer-length-input').trim();
        let input_value = $(input).prop('value');
        input_unit == 'hours'
            ? hours = input_value
            : input_unit == 'minutes'
                ? minutes = input_value
                : input_unit == 'seconds'
                    ? seconds = input_value
                    : null
    })

    time = convertTimeStrToInt(hours, minutes, seconds);

    // time = parseInt(time);
    id_timer_length_field.prop('value', time);
    let val = id_timer_length_field.prop('value');

}

timer_length_increase_btns.find("div").each( (index, btn) => {
    $(btn).on('click', e => {
        let val = $(btn).data("timer-length-increase").trim();
        incrementTime(val);
    })
})

timer_length_decrease_btns.find("div").each( (index, btn) => {
    $(btn).on('click', e => {
        let val = $(btn).data("timer-length-decrease").trim();
        incrementTime(val, decrement=true);
    })
})


const presetCreatePageSetup = () => {
    hideOrShowTimerTypeField();
    setTimerTypeDefault();
    hideOrShowTimerCountdownField();

    // Remove "required" attribute from topics and sub-topics and provide error messages instead
    $("#id_topics").removeAttr('required');
    $("#id_sub_topics").removeAttr('required');

    // Set countdown time based on current timer_length input value
    let val = id_timer_length_field.prop('value')
    let [hours, minutes, seconds] = convertTimeIntToStr(val)
    let timer_length_units = [hours, minutes, seconds]

    // Set timer for spans and inputs
    timer_length_button.find('.btn.btn--outline').find('span').each( (index, span) => {
        $(span).text(timer_length_units[index])
    })
    timer_length_popup_inputs.find('input').each( (index, input) => {
        $(input).prop('value', timer_length_units[index])
    })
}

presetCreatePageSetup();