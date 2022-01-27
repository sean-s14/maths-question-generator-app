const inputs = $(".input");

const acceptable_types = ['text', 'password', 'email', 'number']
inputs.each( (index, input) => {
    $(input).on('change', e => {
        let type = $(input).prop('type');
        acceptable_types.includes(type)
            ? $(input).prop('value').length > 0
                ? $(input).addClass('input__focused')
                : $(input).removeClass('input__focused')
            : null
    })
})