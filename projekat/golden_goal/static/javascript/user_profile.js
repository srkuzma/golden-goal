$(document).ready(function() {
    $(".opened").hide()
    $(".take-presents").hide()

    $(".open-presents").on("click", function() {
        $(".unopened").hide()
        $(".opened").show(1000)
        $(".open-presents").hide()
        $(".take-presents").show()
    })
})
