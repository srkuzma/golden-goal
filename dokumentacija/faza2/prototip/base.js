let header = document.getElementById("my_header")

header.innerHTML = `
<div class="jumbotron bg-dark text-warning jumbotron-fluid">
    <span class="container">
        <span class="row">
            <span class="col-xl-1 col-lg-2 col-md-2 col-sm-12 justify-content-center text-center">
                <a href="index.html">
                    <img src="images/football.png" id="homepage">
                </a>
            </span>
            <span class="col-md-10 col-lg-10 col-xl-11 col-sm-12">
                <span class="row d-none d-xl-block">
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
                        <img src="images/tottenham.png" class="logo">
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
                    <span class="col-9 d-none d-xl-block " style="margin-left: 0px; padding: 0px;">
                        <a class="btn btn-outline-warning first-view" href="played.html" role="button">Rezultati mečeva</a>

                        <a class="btn btn-outline-warning view" href="schedule.html" role="button">Predviđanje ishoda</a>

                        <a class="btn btn-outline-warning view" href="standings.html" role="button">Tabela</a>

                        <a class="btn btn-outline-warning view" href="scorers.html" role="button">Lista strelaca</a>

                        <a class="btn btn-outline-warning view" href="user_rang_list.html" role="button">Rang lista korisnika</a>
                    </span>

                    <span class="col-lg-6 col-md-6 col-sm-3 col-xs-4 d-xl-none" style="margin-top: 35px;">
                        <div class="dropdown">
                            <button class="btn btn-warning dropdown-toggle dropdown-button" role="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Meni
                            </button>

                            <div class="dropdown-menu bg-dark text-warning justify-content-begin" aria-labelledby="dropdownMenuButton">
                                <a class="dropdown-item text-warning bg-dark" href="played.html" role="button">Rezultati mečeva</a>
        
                                <a class="dropdown-item text-warning bg-dark" href="schedule.html" role="button">Predviđanje ishoda</a>
            
                                <a class="dropdown-item text-warning bg-dark" href="standings.html" role="button">Tabela</a>
            
                                <a class="dropdown-item text-warning bg-dark" href="scorers.html" role="button">Lista strelaca</a>
            
                                <a class="dropdown-item text-warning bg-dark" href="user_rang_list.html" role="button">Rang lista korisnika</a>
                            </div>
                        </div>
                    </span>

                    <span class="col-xl-3 d-xl-block d-none text-right" style="padding-left: 0px; padding-right:0px;">
                        <a class="btn btn-outline-warning" id="sign_in" href="sign_in.html" role="button">Uloguj se</a>

                        <a class="btn btn-warning" id="sign_up" href="sign_up.html" role="button">Registruj se</a>
                    </span>

                    <span class="col-lg-6 col-md-6 col-sm-9 col-xs-8 d-xl-none text-right" style="margin-top: 20px;">
                        <a class="btn btn-outline-warning" id="sign_in" href="sign_in.html" role="button">Uloguj se</a>

                        <a class="btn btn-warning" id="sign_up" href="sign_up.html" role="button">Registruj se</a>
                    </span>
                </div>
            </span>
        </span>
    </span>
</div>
`;

let footer = document.getElementById("footer");
footer.innerHTML = `
    <div class="row bg-dark" style="bottom:0; width:100%; position:relative">
    <div class="col bg-dark text-center text-warning" style="margin: 10px; ">
        <h5>Gang of Four &copy; 2022</h5>
    </div>
    </div>
`;

// document.body.appendChild(header.content);
// document.body.appendChild(footer.content);
