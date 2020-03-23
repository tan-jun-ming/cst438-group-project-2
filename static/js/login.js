$(function(){
    $("#login").submit(function(event){
        event.preventDefault();
		let username=$('#UsernameInput').val();
		let password=$('#PasswordInput').val();
		if (username.length > 0 && password.length > 0)
		{
            do_login(username, password);
		}
		else
		{
			alert("All Fields Must be Filled In");
		}


	})
	

})


function do_login(username, password){
	$.ajax({
		method: "POST",
		dataType: 'json',
		url: "/api/login",
    	contentType: 'application/json',
    	data: JSON.stringify( {
			"username": username,
			"password": password,
		}),
        success: function( data, status, jQxhr ){
            localStorage.setItem(token, data.token);
            localStorage.setItem(first_name, data.firstname);
            localStorage.setItem(last_name, data.lastname);
            window.location = "/";
        },
        error: function(jQxhr, status, error){
            alert("Error: " + jQxhr.responseJSON.message);
    }
    })
}