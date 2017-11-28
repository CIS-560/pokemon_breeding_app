//src : https://foundation.zurb.com/forum/posts/48054-autocomplete-search-field

$(document).ready(function() {
    $( '#pokemon-select' ).on('change', setupEggMoves);

    //Disable the selection button on egg moves by default
    $('#search-parents-button').prop('disabled', true);
    $('#egg-move-select').prop('disabled', true);
});

function materialSelectionChanged() {
    $.ajax({
        url: 'api/egg_move/pokemon',
        type: 'POST',
        data: {material: $(this).val()},
        error: function(err) {
            console.log(err);
        },
        success: function(result) {
            setupEggMoves(result.egg_moves);
        }
    });
}

function setupEggMoves(egg_moves) {
    var eggMoveSelect = $( '#egg-move-select' );

    if(!egg_moves.length) {
        // no egg moves found, change the text in the empty option
        eggMoveSelect.append($('<option>No Egg Moves found</option>'));
        return $( '#egg-move-select' ).prop('disabled', true);
    }
    else { 
        for (var i = 0, len = morphologies.length; i < len; i++) {
            eggMoveSelect.append($('<option value="'+ egg_moves[i] + '">' 
                        + egg_moves[i] + '</option>'));
        }
        //re-enable buttons + inputs
        $( '#egg-move-select' ).prop('disabled', false);
        $( '#search-parents-button' ).prop('disabled', false);
    }
}
