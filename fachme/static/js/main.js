// Send a message to the server to be logged
function my_log(string){
    //$.get("ajax/log.php", { log: string } );
}

function format_character(value){
    return (
        $('<div>').append(
            $('<span>').addClass('name').text( value.name ),
            $('<span>').addClass('additional').append(
                $('<span>')
                .addClass('opera')
                .html( value.opera.title ),

                " &bull; ",

                $('<span>')
                .addClass('composer')
                .html( value.opera.composer.name )
            )
        ).html()
    );
}

// Set the user instruction based on the number of characters selected
function update_instructions(){
    if( $('#search-input').tokenInput("get").length == 0 ){
        $(".info").show();
        $("#instructions")
            .html("Name a character that suits <i>your</i> voice");
    }else{
        $("#instructions")
            .html("Add more characters to refine your fach");
    }
}

// Some times the "additional information" is too long. In that case, 
function fit_additional(){
    var n = 100;
    $('span.additional').each( function(){
        var line_height = parseInt($(this).css('line-height'), 10);
        while( line_height < $(this).height() ){
            $(this).css( 'font-size', --n );
        }
    });
}

function show_more(){
    $('#results li.hidden').slice(0, 10).removeClass("hidden");
    if($('#results li.hidden').size() == 0){
        $('#change').hide();
    }else{
        $('#change').show();
    }
    $('#results').show();
    fit_additional();
}

// Write the fach roles to the screen
function populate_fach(data){
    if(data.length > 0){
        $('#fachTitle').html('Roles in your tailor-made fach:');
        $(data).each(function(index, obj) {
            // Store the data
            var $li = $('<li>')
                .addClass('hidden')
                .html( format_character(obj) )
                .append(
                    $('<a>')
                    .addClass('add')
                    .attr('title', 'This role suits my voice')
                    .text('+')
                    .click( function() {
                        my_log('Clicked add button, adding character: ' + obj.id);
                        $("#search-input").tokenInput("add", obj);
                    })
            );

            // Add the Wikipedia link
            if(obj.opera.wikipedia){
                $li.find('.opera').wrapInner(
                    $('<a>')
                        .addClass('operaWikipediaLink')
                        .attr('href', obj.opera.wikipedia)
                        .attr('target', '_blank')
                );
            }

            $('#results').append($li);
        });
    }
}

// Fetch the fach roles from the server
function update_fach(){
    var resumeArray = [];
    for (var key in resume) {
        if(resume[key]){
            resumeArray.push(key);
        }
    }

    // Hide current fach
    $('#results').empty();
    $('#results').hide();
    // Clear the data store
    $('#fachTitle').html('');
    $('#change').hide();
    $('.plea').hide();
    $('.info').hide();
    update_instructions();

    if(resumeArray.length){
        // Set loading message
        $('#fachTitle').html('Faching you gently...');

        $.getJSON('fachme',
            {
                resume: resumeArray.join(','),
                offset: $('#offset').val()
            },
            function(data) {
                if(data.length > 0){
                    populate_fach(data);
                    show_more();
                    $('.plea').show();
                }else{
                    $('#fachTitle')
                    .html('No related characters found,<br /> try adding another character');
                }
            }
        );
    }
}
