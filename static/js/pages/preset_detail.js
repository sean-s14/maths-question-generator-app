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

// View Topics
const view_topics_preset_popup_trigger = $("[data-preset-detail-topics]");
const view_topics_preset_popup = $("#detail_topics_popup");

hidden.on('click', e => {
    hidden.addClass('hidden');
    hidden.removeClass('cover');
    view_topics_preset_popup.addClass('hidden');
})

view_topics_preset_popup_trigger.on('click', e => {
    hidden.removeClass('hidden');
    hidden.addClass('cover');
    view_topics_preset_popup.removeClass('hidden');
    $('#page').css('overflow', 'hidden');
})