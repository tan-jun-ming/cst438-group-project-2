function cartAdd(productid) {
    $.ajax({
        method: "POST",
        dataType: 'json',
        url: "/api/product/"+ productid+"/cart",
        headers: { "Authorization": localStorage.getItem("token") },
        contentType: 'application/json',
        success: function (data, status, jQxhr) {
            //add function to dispaly succes 
        
        },
        error: function (jQxhr, status, error) {
            alert("Error: " + jQxhr.responseJSON.message);
        }
    })
}