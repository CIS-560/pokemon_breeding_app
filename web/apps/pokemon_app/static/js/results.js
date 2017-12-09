$(document).ready(function() {
$(document).foundation();    
    console.log('doc ready');
    var callout = document.getElementById("fav-callout");
    callout.style.visibility = "hidden";   //$('#fav-callout').show().hide();

    //    $('#addToFavorites').attr('disabled', 'disabled');

	document.getElementById("addToFavorites").addEventListener("click", addToFavorites);
    console.log('element hidden');  
});
function addToFavorites() {
    console.log("button clicked");
		var callout = document.getElementById("fav-callout");
    	console.log(document.getElementById("male_pokemon"));

    $('#fav-callout').show();
		callout.style.display = "block";
		callout.style.visibility = "visible";
}
function pokemonSelectionChanged() {
    var str = "";
    var pokemon = "";
    var test ="";
    var source = "static/img/pokemon/"+this.value
    console.log("path " + source);
    $('img').attr("src", source);

    $( "select option:selected" ).each(function() {
        console.log($(this).text());
        str += $( this ).text() + " " + $(this).val();
        pokemon = getFirstWord(str);
    });

    //    alert(str + '\n' + pokemon + '\n' + test);
    $.ajax({
        url: '/egg_moves/',
        type: 'POST',
        data: {'pokemon': pokemon},
        datatype: "json",
        error: function(err) {
            console.log(err);
        },
        success: function(result) {
            setupEggMoves(result.egg_moves);
            console.log(result);
        }
    });
    
        $( '#egg-move-select' ).prop('disabled', false);
}
