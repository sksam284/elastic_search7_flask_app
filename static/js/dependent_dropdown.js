$(document).ready(function() {

//    Get Country Data
    var country, state, city
    $.ajax({
        data : {},
        type : 'GET',
        url : '/get_country',
        beforeSend: function() {
            reset_country_dd()
            set_selected_city_label()
        },
        success: function(data) {
            if (data.error) {
                console.log("Got error")
                if (data.message != undefined) {
                    set_selected_city_label(data.message, 'red')
                }
            }
            else {
                if (data.country != undefined) {
                    $.each(data.country, function(index, value){
                        $('#country_dd').append(new Option(value.name, value.name));
                    })
                }
                set_selected_city_label('Select Country')
            }
        },
        error: function() {
            console.log("Got error for request")
        }
    });

	$("#country_dd").off("change");
    $("#country_dd").on("change", function(){
        country = this.value
        $.ajax({
            data : {
                country: country,
            },
            type : 'GET',
            url : '/get_state',
            beforeSend: function() {
                reset_state_dd()
                set_selected_city_label()
            },
            success: function(data) {
                if (data.error) {
                    console.log("Got error")
                    if (data.message != undefined) {
                        set_selected_city_label(data.message, 'red')
                    }
                }
                else {
                    if (data.state != undefined) {
                        $.each(data.state, function(index, value){
                            $('#state_dd').append(new Option(value.name, value.name));
                        })
                    }
                    set_selected_city_label('Select State')
                }
            },
            error: function() {
                console.log("Got error for request")
            }
        });
    });

	$("#state_dd").off("change");
    $("#state_dd").on("change", function(){
        state = this.value
        $.ajax({
            data : {
                state: state,
            },
            type : 'GET',
            url : '/get_city',
            beforeSend: function() {
                reset_city_dd()
                set_selected_city_label()
            },
            success: function(data) {
                if (data.error) {
                    console.log("Got error")
                    if (data.message != undefined) {
                        set_selected_city_label(data.message, 'red')
                    }
                }
                else {
                    if (data.city != undefined) {
                        $.each(data.city, function(index, value){
                            $('#city_dd').append(new Option(value.name, value.name));
                        })
                    }
                    set_selected_city_label('Select City')
                }
            },
            error: function() {
                console.log("Got error for request")
            }
        });
    });

	$("#city_dd").off("change");
    $("#city_dd").on("change", function(){
        set_selected_city_label('You have selected City: ' + this.value, 'green')
    });

    function reset_country_dd(){
        $("#country_dd").html('<option value="" selected="selected">Select Country</option>')
        reset_state_dd()
    }

    function reset_state_dd(){
        $("#state_dd").html('<option value="" selected="selected">Select State</option>')
        reset_city_dd()
    }

    function reset_city_dd(){
        $("#city_dd").html('<option value="" selected="selected">Select City</option>')
    }

    function set_selected_city_label(data='', color='black'){
        $("#selected_city").html(data).css('color', color)
    }
});
