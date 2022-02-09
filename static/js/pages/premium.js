const hidden = $("[data-account-view-cover]");

const delete_account_popup_trigger = $("[data-delete-account-popup-trigger]");
const delete_account_popup = $("#form_delete_popup");

hidden.on('click', e => {
    hidden.addClass('hidden');
    hidden.removeClass('cover');
    delete_account_popup.addClass('hidden');
})

delete_account_popup_trigger.on('click', e => {
    hidden.removeClass('hidden');
    hidden.addClass('cover');
    delete_account_popup.removeClass('hidden');
    $('#page').css('overflow', 'hidden');
})