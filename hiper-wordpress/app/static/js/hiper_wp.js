$('form[name="produtos"]').on("submit", function(){
    var token = document.getElementById('token').value;
    $.ajax({
        type: "POST",
        url: `/api/produtos`,
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ 'token': token }),
        success: function(response){
            console.log(response)
        }
    })
    return false;
});

$(document).ready(function() {
    $('li.active').removeClass('active');
    $('a[href="' + location.pathname + '"]').closest('li').addClass('active');

    $('[data-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	var checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});

    $("#show_hide_password").on('click', function(event) {
        event.preventDefault();
        if($('.input-group input').attr("type") == "text"){
            $('.input-group input').attr('type', 'password');
            $('.input-group i').addClass( "fa-eye-slash" );
            $('.input-group i').removeClass( "fa-eye" );
        }else if($('.input-group input').attr("type") == "password"){
            $('.input-group input').attr('type', 'text');
            $('.input-group i').removeClass( "fa-eye-slash" );
            $('.input-group i').addClass( "fa-eye" );
        }
    });
});
