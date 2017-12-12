$(document).ready(function() {
$(document).foundation();    
    console.log('doc ready');
    //hide callout
    var callout = document.getElementById("fav-callout");
    callout.style.visibility = "hidden";   //$('#fav-callout').show().hide();

    //    $('#addToFavorites').attr('disabled', 'disabled');

    $.ajaxSetup({
            headers:
            { 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }
        });
    //when the add to fav button is clicked
	document.getElementById("addToFavorites").addEventListener("click", buttonClicked);
});

function addToFavorites() {
	var callout = document.getElementById("fav-callout");
    console.log(document.getElementById("male_pokemon"));

    $('#fav-callout').show();
		callout.style.display = "block";
		callout.style.visibility = "visible";
}

function buttonClicked(child, egg_move) {
    console.log("button clicked");
    //get child
    var sentence = document.querySelector("#sentence").textContent;
    var words = sentence.split(" ");
    var child = words[2];
    var egg_move = words[4];
    console.log("egg move " + egg_move)

    //get parents
    var male_temp = document.getElementById('male_pokemon');
    var temp = male_temp.options[male_temp.selectedIndex].text;
    var temp2 = temp.split(" ");
    var male = temp2[0];
    var level = temp2[3];
    var female_temp = document.getElementById('female_pokemon');
    var female = female_temp.options[female_temp.selectedIndex].text;
    
    $.ajax({
        url: '/add_to_favorites/',
        type: 'POST',
        data: {'male_pokemon': male, 
            'female_pokemon': female, 
            'child': child, 
            'egg_move': egg_move, 
            'level':level},
        datatype: "json",
            error: function (xhr, ajaxOptions, thrownError) {
           console.log(xhr.status);
            console.log(xhr.responseText);
                //console.log(thrownError);
        },
        success: function(result) {
            addToFavorites()
            console.log(result);
        }
    });
}
