let matchday_counter = 0

$(document).ready(function() {
    let load_more = $("#load-more")
    let schedule_table = $(".schedule-table")

    function load_matchdays() {
        $(".schedule-title").hide()
        $(".schedule-table").hide()
        let i

        for(i = 0; i < 5; i++) {
            let id = ".id-" + i

            if($(id)) {
                $(id).show()
            }
            else {
                break
            }
        }

        matchday_counter = i
        let classes = schedule_table.last().attr("class").split(" ")
        let last_id = parseInt(classes[classes.length - 1].split("-")[1])

        if(matchday_counter > last_id) {
            load_more.hide()
        }
    }

    load_matchdays()

    load_more.click(function() {
        for(let i = 0; i < 5; i++) {
            let matchday = matchday_counter + i
            let id = ".id-" + matchday
            $(id).show(2000)
        }

        matchday_counter += 5
        let classes = schedule_table.last().attr("class").split(" ")
        let last_id = parseInt(classes[classes.length - 1].split("-")[1])

        if(matchday_counter > last_id) {
            $(this).hide()
        }
    })
})