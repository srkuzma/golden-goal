$(document).ready(function() {
    $(".like-form").on("submit", function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '../like',
            data: {
                comment_id: $(this).find("button").attr("id").substring(5),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
        })

        let like_counter = $(this).find("button span")
        like_counter.text(parseInt(like_counter.text()) + 1)
    })

    $(".dislike-form").on("submit", function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: '../dislike',
            data: {
                comment_id: $(this).find("button").attr("id").substring(8),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            }
        })

        let dislike_counter = $(this).find("button span")
        dislike_counter.text(parseInt(dislike_counter.text()) + 1)
    })
})
