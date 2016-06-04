var resume = [];

// Activate the main input box
$("#search-input").tokenInput("autocomplete", {
    hintText: "",
    minChars: 1,
    allowFreeTagging: false,
    allowTabOut: false,
    noResultsText: "Try the character's name in the original language",
    searchingText: "<strong id='loading'>Searching<span>.</span><span>.</span><span>.</span></strong>",
    preventDuplicates: true,
    tokenContainer: $("#character-list"),
    placeholder: 'e.g., "Susanna" or "The Countess"',
    resultsFormatter: function(item){
        var r = '<li>' + format_character(item) + '</li>';

        // If this is the first "guess" result, add a label
        if(item.first_guess){
            r = '<li class="result-type">Did you mean?</li>' + r;
        }
        return r;

    },
    tokenFormatter: function(item){
        return '<li><p>' + format_character(item) + '</p></li>';
    },
    onAdd: function (results) {
        resume[results.id] = true;
        $.ajax({
            url: "selected/" + results.id
        });
        my_log("Added character to resume: " + results.id);
        update_fach();
        $(".token-input-input-token input").blur();
    },
    onDelete: function (results) {
        delete resume[results.id];
        my_log("Removed character from resume: " + results.id);
        update_fach();
    },
    onInputChange: function () {
        // Trigger a "Shift" keypress on mouse paste
        var e = jQuery.Event( 'keydown', { which: 16 } );
        $(".token-input-input-token input").trigger(e);
    },
    onInputFocus: function () {
        if (document.documentElement.clientWidth < 479) {
            $('html, body').animate({
                scrollTop: $(".token-input-input-token input").parent().offset().top
            }, 500);
        }
    },
    onInputKeyup: function () {
        if (document.documentElement.clientWidth < 479) {
            $('html, body').animate({
                scrollTop: $(".token-input-input-token input").parent().offset().top
            }, 0);
        }
    }
});

update_instructions();

// Allow users to reveal more results
$("#moreLink").click( function() {
    show_more();
    my_log("Viewed more recomended roles");
    return(false);
});

$('.info-icon').click( function() {
    $(this).toggleClass('active');
    $('.info-text').slideToggle({
        duration: 1000,
        easing: 'linear'
    });
    return false;
});

$('#moreLink').click( function() {
    show_more();
    return false;
});

// If this gets logged, we know we are logging ;)
my_log("Javascript logging works on this machine");

// Google Analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-96948-10']);
_gaq.push(['_trackPageview']);

(function() {
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
