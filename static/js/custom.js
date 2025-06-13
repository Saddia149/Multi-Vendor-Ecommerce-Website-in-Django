$(document).ready(function () {
  $(".increment-btn").click(function (e) {
    e.preventDefault();

    var inc_value = $(this).closest(".product_data").find(".qty-input").val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value < 10) {
      value++;
      $(this).closest(".product_data").find(".qty-input").val(value);
    }
  });

  $(".decrement-btn").click(function (e) {
    e.preventDefault();

    var dec_value = $(this).closest(".product_data").find(".qty-input").val();
    var value = parseInt(dec_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value > 1) {
      value--;
      $(this).closest(".product_data").find(".qty-input").val(value);
    }
  });

  $(".addToCartBtn").click(function (e) {
    e.preventDefault();
    var parentCard = $(this).closest(".product");
    var product_id = parentCard.find(".prod_id").val();
    var product_qty = parentCard.find(".qty-input").val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();

    if (!product_id || !product_qty) {
      alert("Product ID or Quantity is missing!");
      return;
    }

    $.ajax({
      method: "POST",
      url: "/add-to-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        console.log(response);
        alertify.success(response.status);
      },
      error: function (xhr, status, error) {
        console.error(error);
        alertify.error("Something went wrong");
      },
    });
  });

  $(".changeQuantity").click(function (e) {
    e.preventDefault();
    var product_id = $(this).closest(".product_data").find(".prod_id").val();
    var product_qty = $(this).closest(".product_data").find(".qty-input").val();
    var max_qty = $(this).closest(".product_data").find(".max_qty").val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    var is_increment = $(this).hasClass("increment-btn");

    product_qty = parseInt(product_qty);
    max_qty = parseInt(max_qty);

    if (is_increment && product_qty >= max_qty) {
      $(this).closest(".product_data").find(".out-of-stock-msg").show();
      alertify.error("Out of Stock");
      return;
    }

    if (is_increment) {
      product_qty += 1;
    } else {
      product_qty -= 1;
      if (product_qty < 1) product_qty = 1;
    }

    $(this).closest(".product_data").find(".qty-input").val(product_qty);
    $(this).closest(".product_data").find(".out-of-stock-msg").hide();

    $.ajax({
      method: "POST",
      url: "/update-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
      error: function (xhr, errmsg, err) {
        alertify.error("Couldn't update cart");
      },
    });
  });

  $(".addToWishlist").click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product_data").find(".prod_id").val(); // Fixed selector
    var token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      method: "POST",
      url: "/add-to-wishlist",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
      },
      error: function (xhr, status, error) {
        alertify.error("Error occurred.");
        console.error(xhr.responseText);
      },
    });
  });

  $(".delete-cart-item").click(function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product_data").find(".prod_id").val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      method: "POST",
      url: "/delete-cart-item",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.success(response.status);
        $(".cartdata").load(location.href + " .cartdata");
      },
      error: function (xhr, status, error) {
        alertify.error("Something went wrong.");
        console.error(xhr.responseText);
      },
    });
  });

$(document).on('click', '.delete-wishlist-item', function (e) {
  e.preventDefault();
  var product_id = $(this).closest(".product_data").find(".prod_id").val();
  var token = $('input[name="csrfmiddlewaretoken"]').val();

  $.ajax({
    method: "POST",
    url: "/delete-wishlist-item",
    data: {
      product_id: product_id,
      csrfmiddlewaretoken: token,
    },
    success: function (response) {
      alertify.success(response.status);
      $(".wishdata").load(location.href + " .wishdata");
    }
  });
});

 $("#search-input").keyup(function() {
    var query = $(this).val();
    if (query.length >= 1) {
      $.ajax({
        url: "/product-list",
        method: "GET",
        success: function(data) {
          var filtered = data.filter(item => item.toLowerCase().includes(query.toLowerCase()));
          var suggestionBox = $("#suggestion-box");
          suggestionBox.empty();

          if (filtered.length === 0) {
            suggestionBox.append('<div style="padding: 8px;">No products found</div>');
          } else {
            filtered.forEach(function(item) {
              suggestionBox.append('<div class="suggestion-item" style="cursor:pointer;padding:8px;border-bottom:1px solid #eee;">' + item + '</div>');
            });

            // When user clicks a suggestion, redirect to product page
            $(".suggestion-item").click(function() {
              var selectedProduct = $(this).text();
              // Redirect to product detail page via POST form submission or directly build URL if you know pattern
              // Here we send POST by setting input value and submitting form:

              $("#search-input").val(selectedProduct);
              $("#suggestion-box").empty();

              // Submit the form to searchproduct view, which redirects to product detail page
              $("#search-form").submit();
            });
          }
        },
        error: function() {
          $("#suggestion-box").empty();
        }
      });
    } else {
      $("#suggestion-box").empty();
    }
  });

  // Optional: close suggestions if clicked outside
  $(document).click(function(e) {
    if (!$(e.target).closest('#search-input, #suggestion-box').length) {
      $("#suggestion-box").empty();
    }
  });






      $("#product-search").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/product-autocomplete/",
                data: {
                    term: request.term
                },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 1,
        select: function(event, ui) {
            window.location.href = ui.item.url;
        }
    });

    // Handle Enter key press if user types exact product name
    $("#product-search").keydown(function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            const query = $(this).val();
            window.location.href = "/searchproduct?term=" + encodeURIComponent(query);
        }
    });



});
