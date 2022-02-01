$(document).ready( () => {
    const msg_container = $(".message__container");
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
            $(msg).css('pointerEvents', 'none');

            // TODO: Move message container upwards
            // Issues: Try clicking the bottom message and see what happens.
            let h = $(msg).outerHeight(includeMargin=true);
            message.each( (index2, msg2) => {
                if (index2 > index) {
                    let el = elements.item(index2);
                    anime({
                        targets: el,
                        translateY: `-${h * msg_click_count}px`,
                        duration: 300,
                        // delay: 600,
                        easing: 'linear'
                    });
                }
            })

            msg_click_count++;
            if (msg_click_count > elements.length) {
                setTimeout(() => {
                    msg_container.css('display', 'none');
                }, 600);
            }
        })
    })
})