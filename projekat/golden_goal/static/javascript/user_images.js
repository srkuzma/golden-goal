// autori:
// Srdjan Kuzmanovic 0169/2019
// sluzi za prosledjivanje izabrane slike u formu za promenu profilne slike

$(document).ready(function(){
    $(".wrapper button").click(function(){
        $(".wrapper button").removeClass("image-clicked");
        $(this).addClass("image-clicked");
        $("#change_button").prop('value', $(this).attr('id'));
    })
})