let cart_contents = [];

$(function () {
    let user_token = localStorage.getItem("token");

    if (user_token == null) {
        window.location("/login");
        return;
    }

    $("#checkout-button").click(function () {
        do_checkout();
    })

    get_user_cart();
})

function get_user_cart() {
    $.ajax({
        method: "GET",
        dataType: 'json',
        url: `/api/cart`,
        headers: { "Authorization": localStorage.getItem("token") },
        contentType: 'application/json',
        success: function (data, status, jQxhr) {
            cart_contents = data;
            calculate_cart();
        }
    })
}

function calculate_cart() {
    let product_list = $("#product_list");
    product_list.empty();


    let subtotal = 0;

    cart_contents.forEach(function (item) {
        let new_tr = $("<tr></tr>");
        let new_th = $("<th scope=\"row\" class=\"border-0\"></th>");

        new_th.append(
            $("<div class=\"p-2 d-flex flex-column flex-md-row\"></div>"
            ).append($("<img class=\"img-fluid rounded shadow-sm item-img\"/>"
            ).attr("src", item.product.image_url
            ).attr("alt", item.product.name)
            ).append($("<div class=\"ml-3 d-inline-block align-middle\">"
            ).append($("<h5 class=\"mb-0\"> </h5>"
            ).append($("<a class=\"text-dark d-inline-block align-middle\"></a>").text(item.product.name))
            ).append($("<span class=\"text-muted font-weight-normal font-italic d-block\"></span>").text(item.product.details))
            )
        );

        let price = $("<td class=\"border-0 align-middle font-weight-bold\"></td>").text(`$${item.product.price.toFixed(2)}`);
        let quant = $("<td class=\"border-0 align-middle font-weight-bold\"></td>").text(item.amount);

        let delete_button = $("<button type=\"button\" class=\"btn btn-outline-danger\"></button>"
        ).append($("<i class=\"material-icons\"></i>").text("delete")).attr("product_id", item.product.id);

        delete_button.click(function () {
            delete_from_cart(delete_button.attr("product_id"));
        })

        let delete_button_col = $("<td class=\"border-0 align-middle font-weight-bold\"></td>").append(delete_button);

        new_tr.append(new_th).append(price).append(quant).append(delete_button_col);
        product_list.append(new_tr);

        subtotal += item.product.price * item.amount;

    });

    let tax_rate = .10
    let tax = subtotal * tax_rate;

    let total = subtotal + tax;

    $("#subtotal").text(subtotal.toFixed(2));
    $("#tax").text(tax.toFixed(2));
    $("#total").text(total.toFixed(2));


}

function delete_from_cart(product_id) {
    $.ajax({
        method: "DELETE",
        dataType: 'json',
        url: `/api/product/${product_id}/cart`,
        headers: { "Authorization": localStorage.getItem("token") },
        contentType: 'application/json',
        success: function (data, status, jQxhr) {
            get_user_cart();
        },
        error: function (jQxhr, status, error) {
            alert("Error: " + jQxhr.responseJSON.message);
        }
    })

}

function do_checkout() {
    $.ajax({
        method: "PUT",
        dataType: 'json',
        url: `/api/cart/checkout`,
        headers: { "Authorization": localStorage.getItem("token") },
        contentType: 'application/json',
        success: function (data, status, jQxhr) {
            if (data.total_items > 0) {
                alert(`Success!\nYou bought ${data.total_items} items.\n$${data.total_charged.toFixed(2)} has been charged from your account.`)
            }

            get_user_cart();
        },
        error: function (jQxhr, status, error) {
            alert("Error: " + jQxhr.responseJSON.message);
        }
    })
}