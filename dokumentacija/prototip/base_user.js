let template = document.getElementById("my_header")

template.innerHTML = `<div class="jumbotron bg-dark text-warning jumbotron-fluid">
<span class="container">
    <span class="row">
        <span class="col-1">
            <a href="index_user.html">
                <img src="images/football.png" id="homepage">
            </a>
        </span>
        <span class="col-11">
            <span class="row">
                <a href="https://www.arsenal.com/">
                    <img src="images/arsenal.png" class="logo">
                </a>

                <a href="https://www.avfc.co.uk/">
                    <img src="images/aston-vila.png" class="logo">
                </a>

                <a href="https://www.brentfordfc.com/">
                    <img src="images/brentford.png" class="logo">
                </a>

                <a href="https://www.brightonandhovealbion.com/">
                    <img src="images/brighton.png" class="logo">
                </a>

                <a href="https://www.burnleyfootballclub.com/">
                    <img src="images/burnley.png" class="logo">
                </a>

                <a href="https://www.chelseafc.com/en">
                    <img src="images/chelsea.png" class="logo">
                </a>

                <a href="https://www.cpfc.co.uk/">
                    <img src="images/crystal-palace.png" class="logo">
                </a>

                <a href="https://www.evertonfc.com/home">
                    <img src="images/everton.png" class="logo">
                </a>

                <a href="https://www.leedsunited.com/">
                    <img src="images/leeds.png" class="logo">
                </a>
                
                <a href="https://www.lcfc.com/">
                    <img src="images/leicester.png" class="logo">
                </a>

                <a href="https://www.liverpoolfc.com/">
                    <img src="images/liverpool.png" class="logo">
                </a>
                
                <a href="https://www.mancity.com/">
                    <img src="images/manchester-city.png" class="logo">
                </a>
                
                <a href="https://www.manutd.com/">
                    <img src="images/manchester-united.png" class="logo">
                </a>

                <a href="https://www.nufc.co.uk/">
                    <img src="images/newcastle.png" class="logo">
                </a>

                <a href="https://www.canaries.co.uk/">
                    <img src="images/norwitch.png" class="logo">
                </a>
                
                <a href="https://www.southamptonfc.com/">
                    <img src="images/southampton.png" class="logo">
                </a>
                
                <a href="https://www.tottenhamhotspur.com/">
                    <img src="images/tottenhamp.png" class="logo">
                </a>

                <a href="https://www.watfordfc.com/">
                    <img src="images/watford.png" class="logo">
                </a>
                
                <a href="https://www.whufc.com/">
                    <img src="images/westham.png" class="logo">
                </a>
                
                <a href="https://www.wolves.co.uk/">
                    <img src="images/wolves.png" class="logo">
                </a>
            </span>
            <div class="row">
                <span class="col-9" style="margin-left: 0px;">
                    <a class="btn btn-outline-warning"style="font-size: 20px; border: 0px;" href="played_user.html" role="button">Rezultati mečeva</a>

                    <a class="btn btn-outline-warning view" href="schedule_user.html" role="button">Predviđanje ishoda</a>

                    <a class="btn btn-outline-warning view" href="standings_user.html" role="button">Tabela</a>

                    <a class="btn btn-outline-warning view" href="scorers_user.html" role="button">Lista strelaca</a>

                    <a class="btn btn-outline-warning view" href="user_rang_list_user.html" role="button">Rang lista korisnika</a>
                </span>

                <span class="col">
                    <a id="username" class="btn btn-outline-warning" href="user_profile.html" role="button"><img src="images/manchester-united.png" id="user_icon"> kovacd</a>

                    <a class="btn btn-warning" href="index.html" id="log_out" role="button">Izloguj se</a>
                </span>
            </div>
        </span>
    </span>
</span>
</div>`;

document.body.appendChild(template.content);