let matchday_counter = 0

$(document).ready(function() {
    let load_more = $("#load-more")
    let schedule_table = $(".schedule-table")

    function get_color(prediction, home_score, away_score){
        if (prediction == '')
            return 'gray-res'

        let result;
        let diff = home_score - away_score;
        if (diff > 0)
            result = '1'
        else if (diff == 0)
            result = 'X'
        else
            result = '2';

        if (result == prediction)
            return 'green-res';
        else
            return 'red-res';
    }


    $.ajax({
            url: '/live_results',
            dataType: 'json',
            type: 'GET',
        }).done(function(response) {
            let live_matchdays = JSON.parse(response)
            for(let i = 0; i < live_matchdays.length; i++){
                let games = live_matchdays[i]["games"];
                for (let j = 0; j < games.length; j++){
                    let prediction = games[j]['prediction']
                    let home_score = games[j]['home_team_score']
                    let away_score = games[j]['away_team_score']
                    let id = games[j]['id']
                    $("#" + id).removeClass().addClass(get_color(prediction, home_score, away_score));
                }
            }
        })



    function get_results_live(){
        setInterval(function() {
            $.ajax({
                url: '/live_results',
                dataType: 'json',
                type: 'GET',
            }).done(function(response) {
                let live_matchdays = JSON.parse(response)

                let live_matchdays_div = $("#live_matchdays")
                live_matchdays_div.empty();

                for(let i = 0; i < live_matchdays.length; i++){
                    let h1 = $("<h1>").addClass("text-center").addClass("matchday").text("Matchday " + live_matchdays[i]['matchday'])
                    let table = $("<table>").addClass("table").addClass("table-striped").addClass("table-dark")
                        .addClass("rounded").addClass("text-center");
                    let thead = $("<thead>")
                    let tr = $("<tr>").addClass("text-warning").addClass("rounded")
                    let home = $("<th>").addClass("border-zero").addClass("rounded-left").addClass("col-5").addClass("bottom-left-zero-radius")
                        .text("Home team")
                    let result = $("<th>").addClass("border-zero").addClass("col-2").text("Result");
                    let away = $("<th>").addClass("border-zero").addClass("rounded-left").addClass("col-5").addClass("bottom-left-zero-radius")
                        .text("Away team")

                    tr.append(home).append(result).append(away)
                    thead.append(tr)

                    let games = live_matchdays[i]["games"];
                    let tbody = $("<tbody>")
                    for (let j = 0; j < games.length; j++){
                        let game_tr = $("<tr>")
                        let prediction = games[j]['prediction']
                        let home_score = games[j]['home_team_score']
                        let away_score = games[j]['away_team_score']
                        let colorClass = get_color(prediction, home_score, away_score)
                        game_tr.append($("<td>").prop('align','right').addClass("col-5").append(games[j]['home_team'] + " ").append($("<img>").addClass("crest").prop('alt', '').prop('src', '/static/' + games[j]['home_team_crest'])))
                        game_tr.append($("<td>").prop('align','center').addClass("col-2").append($("<div>").attr('id', games[j]['id']).addClass(colorClass).text(games[j]['home_team_score'] + " : " + games[j]['away_team_score'])))
                        game_tr.append($("<td>").prop('align','left').addClass("col-5").append($("<img>").addClass("crest").prop('alt', '').prop('src', '/static/' + games[j]['away_team_crest'])).append(" " + games[j]['away_team']))
                        tbody.append(game_tr)
                    }
                    tbody.append($("<tr>").addClass("rounded"))

                    table.append(thead)
                    table.append(tbody)
                    live_matchdays_div.append(table)
                }

                if (live_matchdays.length == 0){
                    live_matchdays_div.append($("<h2>").addClass("text-center").addClass("no-games").text("There are currently no live games."))
                }
            });
        }, 10000)
    }

    get_results_live();

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
            $(this).prop('checked', false)
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

