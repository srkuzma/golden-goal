// autori:
// Dejan Kovacevic 0167/2019
// sluzi za ucitavanja dodatnih vesti iz liste svih vesti

let news_counter = 0

$(document).ready(function() {
    let load_more = $("#load-more")
    let news = $(".news")

    function load_news() {
        news.hide()
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

        news_counter = i
        let classes = news.last().attr("class").split(" ")
        let last_id = parseInt(classes[classes.length - 1].split("-")[1])

        if(news_counter > last_id) {
            load_more.hide()
        }
    }

    load_news()

    load_more.click(function() {
        for(let i = 0; i < 5; i++) {
            let news = news_counter + i
            let id = ".id-" + news
            $(id).show(2000)
        }

        news_counter += 5
        let classes = news.last().attr("class").split(" ")
        let last_id = parseInt(classes[classes.length - 1].split("-")[1])

        if(news_counter > last_id) {
            $(this).hide()
        }
    })
})