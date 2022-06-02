// autori:
// Dejan Kovacevic 0167/2019
// Srdjan Kuzmanovic 0169/2019
// sluzi za azuriranje rezultata utakmica uzivo bez osvezavanja index.html stranice

setInterval(function() {
    $.ajax({
        url: 'live_games_index',
        dataType: 'json',
        type: 'GET',
    }).done(function(response) {
        let live_games_tbody = $("#live_games")
        live_games_tbody.empty()
        let matches = JSON.parse(response)
        let live_games = []

        for(let i = 0; i < matches.length; i++) {
            live_games.push({
                home_team: matches[i]['home_team'],
                away_team: matches[i]['away_team'],
                home_team_score: matches[i]['home_team_score'],
                away_team_score: matches[i]['away_team_score'],
            })
        }

        for(let i = 0; i < live_games.length; i++) {
            let game_tr = $("<tr>")

            game_tr.append($("<td>").addClass("col-5").text(live_games[i].home_team))
            game_tr.append($("<td>").addClass("col-2").text(live_games[i].home_team_score + " : " + live_games[i].away_team_score))
            game_tr.append($("<td>").addClass("col-5").text(live_games[i].away_team))
            live_games_tbody.append(game_tr)
        }

        let last_tr = $("<tr>").addClass("rounded")

        if(live_games.length > 0) {
            let plus = $("<td>").addClass("text-center").addClass("justify-content-center").addClass("rounded-bottom").addClass("plus-td").attr("colspan", "3")
            plus.append($("<a>").addClass("btn").addClass("btn-outline-warning").addClass("plus").attr({
                "href": "prediction",
                "role": "button"
            }).text("+"))
            last_tr.append(plus)
        }
        else {
            let plus = $("<td>").addClass("text-center").addClass("justify-content-center").addClass("rounded-bottom").addClass("text-warning").addClass("no-games").attr("colspan", "3")
            plus.append($("<h5>").text("No live games"))
            last_tr.append(plus)
        }

        live_games_tbody.append(last_tr)
    });
}, 10000)
