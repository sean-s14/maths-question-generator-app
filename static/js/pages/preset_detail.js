const preset_detail_topics_popup_btn = $("[data-preset-detail-topics]");
const preset_detail_topics_popup = $("#detail_topics_popup");
const preset_detail_hidden_cover = $("[data-preset-detail-cover]");

preset_detail_topics_popup_btn.on('click', e => {
    preset_detail_hidden_cover.removeClass("hidden");
    preset_detail_topics_popup.removeClass("hidden");
})

preset_detail_hidden_cover.on('click', e => {
    preset_detail_hidden_cover.addClass("hidden");
    preset_detail_topics_popup.addClass("hidden");
})