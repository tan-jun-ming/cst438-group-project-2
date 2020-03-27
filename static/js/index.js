let product_data = {}
let logged_in = false;

$(function () {
    $("#searchform").submit(function (event) {
        event.preventDefault();
        alert("You searched for: " + $(event.target).find("input").val() + "\nThis feature is not yet implemented.");

    })

    let user_token = localStorage.getItem("token");

    if (user_token != null) {
        logged_in = true;

        let firstname = localStorage.getItem("firstname");
        let lastname = localStorage.getItem("lastname");

        $("#login_button").text(`${firstname} ${lastname}`);
        $("#login_button").attr("href", "account");
    }

    $("#cart-add-button").click(function () {
        if (logged_in && !$("#cart-add-button").hasClass("disabled")) {
            add_to_cart($("#cart-add-button").attr("product_id"));
            disable_cart_button();
        }
    })
    get_random_products();
})

function get_random_products() {
    $.ajax({
        method: "GET",
        dataType: 'json',
        url: "/api/products",
        contentType: 'application/json',
        success: function (data, status, jQxhr) {
            $("#product-grid").empty();
            product_data = {}

            data.forEach(function (item) {
                product_data[item.id] = item

                let new_item_holder = $("<div></div>");
                new_item_holder.addClass("store-item d-flex flex-column justify-content-end");

                let new_item = $("<div></div>");
                new_item.addClass("store-item-image");
                new_item.css("background-image", `url(${item.image_url})`);

                let item_name = $("<span></span>");
                item_name.addClass("store-item-name");
                item_name.text(item.name);

                new_item_holder.append(item_name);
                new_item_holder.append(new_item);

                new_item_holder.click(function () {
                    open_modal(item.id);
                })

                $("#product-grid").append(new_item_holder)
            })
        }
    })
}

function add_to_cart(product_id) {
    $.ajax({
        method: "PUT",
        dataType: 'json',
        url: `/api/product/${product_id}/cart`,
        headers: { "Authorization": localStorage.getItem("token") },
        contentType: 'application/json',
    })
}

function open_modal(product_id) {
    product = product_data[product_id];

    $("#modal-product-name").text(product.name);
    $("#modal-product-img").attr("src", product.image_url);
    $("#modal-product-desc").text(product.details);
    $("#modal-product-price").text(product.price.toFixed(2));

    if (logged_in) {
        $("#cart-add-button").attr("product_id", product.id);
        reset_cart_button();
    } else {
        disable_login_cart_button();
    }


    $("#product-modal").modal();
}

function reset_cart_button() {
    $("#cart-add-button").removeClass("disabled");
    $("#cart-add-button").text("Add to cart");
}

function disable_cart_button() {
    $("#cart-add-button").addClass("disabled");
    $("#cart-add-button").text("Added!");
}

function disable_login_cart_button() {
    $("#cart-add-button").addClass("disabled");
    $("#cart-add-button").text("Add to cart");
    $("#cart-add-button").attr("data-toggle", "tooltip");
    $("#cart-add-button").attr("title", "Log in to add to cart!");
    $("#cart-add-button").tooltip()
}