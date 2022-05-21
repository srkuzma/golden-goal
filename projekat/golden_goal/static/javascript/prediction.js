let matchday_counter = 0

$(document).ready(function() {
    function load_matchdays() {
        $(".schedule-title").hide()
        $(".schedule-table").hide()

        for(let i = 0; i < 5; i++) {
            let matchday = matchday_counter + i
            let id = ".id-" + matchday
            $(id).show()
        }

        matchday_counter = 5
    }

    load_matchdays()

    $("#load-more").click(function() {
        for(let i = 0; i < 5; i++) {
            let matchday = matchday_counter + i
            let id = ".id-" + matchday
            $(id).show(2000)
        }

        matchday_counter += 5
        let classes = $(".schedule-table").last().attr("class").split(" ")
        let last_id = parseInt(classes[classes.length - 1].split("-")[1])

        if(matchday_counter > last_id) {
            $(this).hide()
        }
    })
})