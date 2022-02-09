// Causes div with opacity of 0.5 to cover screen until clicked on or until side-nav closes

const nav_toggle = $(".nav__toggle");  // Button to toggle side-nav
const menu_toggle = $("#menu-toggle");  // Checkbox for side-nav
const base_hidden_cover = $("[data-base-hidden-cover]");  // Cover to close side-nav

nav_toggle.on('click', e => {
    let isMenuActive = menu_toggle.prop('checked');

    // isMenuActive
    //     ? base_hidden_cover.addClass('hidden')
    //     : base_hidden_cover.removeClass('hidden')
    base_hidden_cover.removeClass('hidden');

    if ( isMenuActive ) {
        base_hidden_cover.css('opacity', 0);
        base_hidden_cover.css('pointerEvents', 'none');
    } else {
        base_hidden_cover.css('opacity', 0.5);
        base_hidden_cover.css('pointerEvents', 'all');
    }
})

base_hidden_cover.on('click', e => {
    nav_toggle.trigger('click');
})


const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');