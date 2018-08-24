$(document).ready(function () {
    // Init
    $('.loader').hide();
    $('#result').hide();
    console.log("init");
    // Predict
    $('#btn-generate').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        // Show loading animation
        console.log(form_data);
        $(this).hide();
        $('.loader').show();
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/generate',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                console.log(data);
                document.getElementById('result').src = data;
                console.log('Success!');
                $('#btn-generate').show();
            },
        });
        
    });
});
