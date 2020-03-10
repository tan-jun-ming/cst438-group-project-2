$(function(){
    $("#CreateAccount").submit(function(event){
        event.preventDefault();
		let firstPass=$('#PasswordInput').val();
		let secondPass=$('#RepeatPasswordInput').val();
		if (firstPass==secondPass){	
			if (/[a-z]/.test(firstPass)&&/[A-Z]/.test(firstPass)&&/[0-9]/.test(firstPass)){
				alert("Valid Password");
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
    })
})