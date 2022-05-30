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

    $(":radio").click(function(){
        let label = $(this).next();

        $(":radio").filter(function(){
            return $(this).prop('checked') === false && $(this).prop('disabled') === false;
        }).next().addClass("red-pred");

        if (label.hasClass('red-pred')) {
            label.removeClass('red-pred');
        }
        else {
            label.addClass('red-pred')
        }
    })

    $("#predict-form").on('submit',
        function(e){
            e.preventDefault();
            let buttonsObject = $("label").filter(function() {
               return $(this).css('background-color') === 'rgb(17, 155, 21)';
            }).css({'background-color':'goldenrod'}).map(function(){
                return this.getAttribute('for');
            });
            let buttons = []
            for (let button of buttonsObject){
                buttons.push(button);
                console.log(button)
                let game_id = $('#' + button).attr('id').split('-')[2];
                // console.log(game_id)
                let group = "name-" + game_id;
                $("input[name=" + group + "]").attr('disabled', true)
            }

            $.ajax({
              type: 'POST',
              url:'predict_match/',
              dataType: 'json',
              data:{
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                  'buttons': JSON.stringify(buttons)
              }
            })
        }
    )

    function addForType(type){
        let n;
        switch(type){
            case '1':
                n = 1;
                break;
            case 'X':
                n = 2;
                break;
            case '2':
                n = 3;
                break;
        }
        $(".type-" + type + " label").removeClass('red-pred')
        console.log("REMOVED")
        $(".type-" + type + " label:nth-of-type(" + n + ")").css({'background-color':'goldenrod'});
        $(".type-" + type + " input").prop('disabled', true);
    }

    function addPredictions(){
        types = ["1", "X", "2"];
        for(let type of types){
            addForType(type);
        }
    }

    addPredictions();

})

