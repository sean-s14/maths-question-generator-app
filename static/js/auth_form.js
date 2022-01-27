const auth_form = $(".auth__form");

auth_form.find('input').each( (index, input) => {
    if (index == 0 ) { return };
    $(input).on('change', e => {
        console.log($(input).prop('value'));
        $(input).prop('value').length > 0
            ? $(input).addClass('auth__form__focused')
            : $(input).removeClass('auth__form__focused')
    })
})