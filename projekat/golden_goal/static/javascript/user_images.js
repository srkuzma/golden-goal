$(document).ready(function(){
    $(".wrapper button").click(function(){
        $(".wrapper button").removeClass("image-clicked");
        $(this).addClass("image-clicked");
        $("#change_button").prop('value', $(this).attr('id'));
    })
})