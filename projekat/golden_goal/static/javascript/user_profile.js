$(document).ready(function() {
    $(".opened").hide();
    $(".take-presents").hide();

    function hide_element(element, index) {
        setTimeout(function() {
            element.hide();
        }, index * 1000)
    }

    function show_element(element, index) {
        setTimeout(function() {
            element.show(1000);
        }, index * 1000)
    }

    $(".open-presents").on("click", function() {
        $(".unopened").each(function(index) {
            hide_element($(this), index)
        })

        $(".opened").each(function(index) {
            show_element($(this), index)
        })

        $(".open-presents").hide();
        $(".take-presents").show();
    })
})
