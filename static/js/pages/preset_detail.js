const hidden = $("[data-preset-view-cover]");

const delete_preset_popup_trigger = $("[data-delete-preset-popup-trigger]");
const delete_preset_popup = $("#form_delete_popup");

hidden.on('click', e => {
    hidden.addClass('hidden');
    hidden.removeClass('cover');
    delete_preset_popup.addClass('hidden');
})

delete_preset_popup_trigger.on('click', e => {
    hidden.removeClass('hidden');
    hidden.addClass('cover');
    delete_preset_popup.removeClass('hidden');
    $('#page').css('overflow', 'hidden');
})