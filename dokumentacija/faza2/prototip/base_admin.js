let header = document.getElementById("my_header")

header.innerHTML = `
<div class="jumbotron bg-dark text-warning jumbotron-fluid">
    <span class="container">
        <span class="row">
            <span class="col-xl-1 col-lg-2 col-md-2 col-sm-12 justify-content-center text-center">
                <a href="index_admin.html">
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
                    <span class="col-9 d-none d-xl-block " style="margin-left: 0px;  padding: 0px">
                        <a class="btn btn-outline-warning first-view" href="played_admin.html" role="button">Rezultati mečeva</a>
        
                        <a class="btn btn-outline-warning view" href="standings_admin.html" role="button">Tabela</a>

                        <a class="btn btn-outline-warning view" href="scorers_admin.html" role="button">Lista strelaca</a>

                        <a class="btn btn-outline-warning view" href="user_rang_list_admin.html" role="button">Rang lista korisnika</a>
                    </span>

                    <span class="col-lg-6 col-md-6 col-sm-3 col-xs-4 d-xl-none" style="margin-top: 35px;">
                        <div class="dropdown">
                            <button class="btn btn-warning dropdown-toggle dropdown-button" role="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Meni
                            </button>

                            <div class="dropdown-menu bg-dark text-warning justify-content-begin" aria-labelledby="dropdownMenuButton">
                                <a class="dropdown-item text-warning bg-dark" href="played_admin.html" role="button">Rezultati mečeva</a>
                    
                                <a class="dropdown-item text-warning bg-dark" href="standings_admin.html" role="button">Tabela</a>
            
                                <a class="dropdown-item text-warning bg-dark" href="scorers_admin.html" role="button">Lista strelaca</a>
            
                                <a class="dropdown-item text-warning bg-dark" href="user_rang_list_admin.html" role="button">Rang lista korisnika</a>
                            </div>
                        </div>
                    </span>

                    <span class="col-xl-3 d-xl-block d-none text-right" style="padding-left: 0px; padding-right: 0px;">
                        <a id="username" class="btn btn-outline-warning" style="padding: 5px;" href="admin_profile.html" role="button"><img src="images/manchester-united.png" id="user_icon"> kovacd</a>

                        <a class="btn btn-warning" href="index.html" id="log_out" role="button">Izloguj se</a>
                    </span>

                    <span class="col-lg-6 col-md-6 col-sm-9 col-xs-8 d-xl-none text-right" style="margin-top: 20px;">
                        <a id="username" class="btn btn-outline-warning" href="admin_profile.html" role="button"><img src="images/manchester-united.png" id="user_icon"> kovacd</a>

                        <a class="btn btn-warning" href="index.html" id="log_out" role="button">Izloguj se</a>
                    </span>
                </div>
            </span>
        </span>
    </span>
</div>
`;

let footer = document.getElementById("footer");
footer.innerHTML = `
    <div class="row bg-dark">
    <div class="col bg-dark text-center text-warning" style="margin: 10px;">
        <h5>Gang of Four &copy; 2022</h5>
    </div>
    </div>
`;

// document.body.appendChild(header.content);
// document.body.appendChild(footer.content);
