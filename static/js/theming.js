$(document).ready(() => {

    const change_theme_btn = $("#change_theme");

    const invert_theme = () => {
        // Matches all elements with an attribute of "class" that contain the string "light"
        const light_themed_el = $("*[class*=light]");
        const dark_themed_el = $("*[class*=dark]");
        let all_elements = light_themed_el.add(dark_themed_el);

        const change_classes = (el) => {
            // Return array of all classes in element
            let current_el_class = $(el).attr('class').split(' ');
            let new_el_class = [];

            // Loop through classes swapping 'dark' with 'light' and vice versa
            current_el_class.forEach(cls => {
                let new_cls = cls.includes('dark')
                    ? cls.replace(/dark/g, 'light')
                    : cls.replace(/light/g, 'dark')
                new_el_class.push(new_cls)
            });
            new_el_class = new_el_class.join(' ');            

            $(el).removeClass(current_el_class);  // Remove old classes
            $(el).addClass(new_el_class);  // Add new classes
        }

        all_elements.each((index, el) => change_classes(el) );
    }

    const change_theme = () => {
        console.log('Change theme working!')
        const theme = localStorage.getItem('theme');
    
        if ( theme === 'dark' || theme === null) {
            invert_theme();
            localStorage.setItem('theme', 'light');
        } else if ( theme === 'light' ) {
            invert_theme();
            localStorage.setItem('theme', 'dark');
        }
    }
    change_theme_btn.on('click', e => change_theme() );

    const theme_initial_load = () => {
        // If local storage's "theme" is "dark" then invert themes
        const theme = localStorage.getItem('theme');

        theme === 'light'
            ? invert_theme()
            : null;
    }

    theme_initial_load();

    // Hide loading icon
    setTimeout(() => $("#loading-screen").css('display', 'none'), 500);  // Maybe remove settimeout?
    // $(".loading-icon").css('display', 'none');
})