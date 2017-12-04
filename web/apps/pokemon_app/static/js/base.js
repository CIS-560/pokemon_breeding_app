$(document).ready(function() {
    $("#egg-move-select").attr('disabled','disabled'); // disable
    $("#search-parents-button").attr('disabled','disabled'); // disable
    console.log("test");
    $.ajaxSetup({
            headers:
            { 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }
        });
    $("#pokemon-select").on('change',pokemonSelectionChanged);
    $('##pokemon-select').change(function() {
          $('#poke-pic').attr("src",this.value);
    });
    $("#egg-move-select").on('change', function() {
    $( '#search-parents-button' ).prop('disabled', false);
    });
});
function pokemonSelectionChanged() {
    var str = "";
    var pokemon = "";
    var test ="";

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

function setupEggMoves(egg_moves) {
    var eggMoveSelect = $( '#egg-move-select' );


    if(!egg_moves.length) {
        // no egg moves found, change the text in the empty option
        eggMoveSelect.append($('<option>No Egg Moves found</option>'));
        return $( '#egg-move-select' ).prop('disabled', true);
    }
    else { 
        for (var i = 0, len = egg_moves.length; i < len; i++) {
            eggMoveSelect.append($('<option value="'+ egg_moves[i] + '">' 
                        + egg_moves[i] + '</option>'));
        }
    }
}

function showimage()
{
    if (!document.images)
    return
    document.images.pictures.src=
    document.mygallery.picture.options[document.mygallery.picture.selectedIndex].value
}
function getFirstWord(str) {
        let spacePosition = str.indexOf(' ');
        if (spacePosition === -1)
            return str;
        else
            return str.substr(0, spacePosition);
    };
