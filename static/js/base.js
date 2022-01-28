// Causes div with opacity of 0.5 to cover screen until clicked on or until side-nav closes

const nav_toggle = $(".nav__toggle");  // Button to toggle side-nav
const menu_toggle = $("#menu-toggle");  // Checkbox for side-nav
const base_hidden_cover = $("[data-base-hidden-cover]");  // Cover to close side-nav

nav_toggle.on('click', e => {
    let isMenuActive = menu_toggle.prop('checked');

    isMenuActive
        ? base_hidden_cover.addClass('hidden')
        : base_hidden_cover.removeClass('hidden')
})

base_hidden_cover.on('click', e => {
    nav_toggle.trigger('click');
})