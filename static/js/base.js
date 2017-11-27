//src : https://foundation.zurb.com/forum/posts/48054-autocomplete-search-field
$( '#iconTag' ).autocomplete({
    source: availableTags = ["rendered list of pokemons", "pokemons", "porygon", "porygon2", "pikachu"];
    minLength: 3,
    appendTo: "frmCriteria"
});
