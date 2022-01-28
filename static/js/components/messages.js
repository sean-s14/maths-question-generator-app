$(document).ready( () => {
    const msg_container = $(".message__container");
    // msg_container.css('opacity', 1)
    anime({
        targets: '.message__container',
        opacity: 1,
        duration: 3000
    })
    const message = $(".message");
    let msg_click_count = 1;
    message.each( (index, msg) => {
        $(msg).on('click', e => {
            console.log('Closed');
            let elements = document.getElementsByClassName('message');
            let el = elements.item(index);
            anime({
                targets: el,
                scale: 0,
                duration: 100,
                easing: 'linear'
            });

            // TODO: Move message container upwards
            // Issues: Try clicking the bottom message and see what happens.
            let h = $(msg).outerHeight(includeMargin=true);
            anime({
                targets: '.message__container',
                translateY: `-${h * msg_click_count}px`,
                delay: 600
            });

            msg_click_count++;
        })
    })
})