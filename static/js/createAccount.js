$(function(){
    $("#CreateAccount").submit(function(event){
        event.preventDefault();
		let firstName=$('#FirstNameInput').val();
		let lastName=$('#LastNameInput').val();
		let userName=$('#UsernameInput').val();
		let firstPass=$('#PasswordInput').val();
		let secondPass=$('#RepeatPasswordInput').val();
		if (firstName.length > 0 && lastName.length > 0 && userName.length > 0 && firstPass.length > 0 && secondPass.length > 0)
		{
			if (firstPass==secondPass){	
				if (/[a-z]/.test(firstPass)&&/[A-Z]/.test(firstPass)&&/[0-9]/.test(firstPass)){
					do_create_account(userName, firstPass, firstName, lastName);
				}
				else
				{
					alert("Invalid Password, Enter at Least 1 Lowercase, 1 Uppercase and 1 Number");
				}
			}
			else
			{
				alert("Password Rentry Failed");
			}
		}
		else
		{
			alert("All Fields Must be Filled In");
		}


	})
	

})

function do_create_account(username, password, firstname, lastname){
	$.ajax({
		method: "POST",
		dataType: 'json',
		url: "/api/create_account",
    	contentType: 'application/json',
    	data: JSON.stringify( {
			"username": username,
			"password": password,
			"firstname": firstname,
			"lastname": lastname
		}),
		success: function( data, status, jQxhr ){
			alert("Account creation successful. Please log in to continue.");
			window.location = "/login";
		},
	  })
}