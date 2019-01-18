var Cart = [];
console.log(Cart);
if (localStorage.getItem("Cart") != null) {
    Cart = JSON.parse(localStorage.getItem("Cart"));
} else {
    localStorage.setItem("Cart", "[]");
}

//declare an empty array for temporary use
var tempArray = [];

//function to render featured products on the homepage
function renderFeaturedproducts(products) {
    console.log(products);
    products = products.reverse();
    for (var i = 0; i < products.length; i++) {
        name = products[i].Name;
        price = products[i].Price;
        id = products[i].id;
        quantity = products[i].Quantity;
        Category = products[i].Category;
        image_link = products[i].Image;
        productTab = $("<div id='productTab'><img src='http://res.cloudinary.com/jalome/image/upload/c_fill,h_240,w_240/" + image_link + "'/> <p id='name'>" + name + "</p><p id='category'>" + Category + "</p><p id='price'>R" + price + "</p> <button onclick='displayImg("+id+")'>View product</button></div>");
        $("#featuredProducts").append(productTab);

    }
}

//select category function, highlight the selected category..
function selectCat(sender) {
    console.log(sender.id);
    $(".selected").removeClass();
    $("#" + sender.id).addClass("selected");
    getCategory(sender.id);


}

function getProducts() {
    $("#rightPane").html("");
    $("#rightPane").css("height", "auto");
    renderShopOptions();
    if (window.innerWidth <= 1000) {
        var menuIcon = document.getElementById("menuIcon");
        menuIcon.setAttribute("src", "/static/website/menu.svg");
        $("#leftPane").css("height", "50px");
        $("#menuIcon").addClass("animated rotateIn").one("webkitAnimationEnd", function () {
            $("#menuIcon").removeClass();
        });
        $("#leftPane").addClass("menuUnExtend").one('webkitAnimationEnd', function () {
            $("#leftPane").removeClass();
        });
        var menuLists = $(".menuList");
        console.log(menuLists);
        for (var x = 0; x < menuLists.length; x++) {
            menuLists[x].style.display = 'none';
        }
    }
}

//render shop products
function renderproducts(products, infoImg) {
    products = shuffleArray(products);
    $("#products").html("");
    var Footer = "<footer><div id='author'><p>Website developed by Jalome Chirwa</p></div><div id='socialIcon'><span>Social media links:</span><a href='https://www.instagram.com/i_am_soap/' target='_blank'><i class='fa fa-instagram'></i></a><a href='https://twitter.com/i_am_SOAP_ZA' target='_blank'><i class='fa fa-twitter'></i></a><i class='fa fa-facebook'></i></div></footer>";
    for (var i = 0; i < products.length; i++) {
        name = products[i].Name;
        price = products[i].Price;
        id = products[i].id;
        quantity = products[i].Quantity;
        Category = products[i].Category;
        image_link = products[i].Image;
        productTab = $("<div id='productTab'><img onclick='displayImg(" + id + ")' id='info' src=" + infoImg + "><img src='http://res.cloudinary.com/jalome/image/upload/c_fill,h_240,w_240/" + image_link + "'/> <p id='name'>" + name + "</p><p id='category'>" + Category + "</p><p id='price'>R" + price + "</p> <button id='" + id + "Button' onclick='addToCart(" + id + ")'>Add to cart</button></div>");
        $("#products").append(productTab);

    }
    $("#products").append(Footer);
    if (Cart != null) {
        $("#Count").html("");
        $("#Count").html(Cart.length);
    }
}

function renderProductInfo(data) {
    $("#view_product_image").attr("src", "http://res.cloudinary.com/jalome/image/upload/c_fill,h_350,w_350/" + data[0].Image);
    $("#view_product_desc").append("<p onclick='closePreview()' id='closePreview'>close</p>");
    $("#view_product_desc").append("<h1>" + data[0].Name + "</h1>");
    $("#view_product_desc").append("<span><font>Category:</font> <span id='infoSpan'>" + data[0].Category + "</span></span><br>");
    $("#view_product_desc").append("<span><font>Price:</font> <span id='infoSpan'>R" + data[0].Price + "</span></span><br>");
    $("#view_product_desc").append("<span><font>In stock:</font> <span id='infoSpan'>" + data[0].Quantity + " products</span></span><br>");
    $("#view_product_desc").append("<p id='description'>" + data[0].desc + "</p>");
    $("#view_product_desc").append("<button class='' id='" + data[0].id + "Button' onclick='addToCart(" + data[0].id + ")'>Add to cart</button>");
}

function closePreview() {
    $("#productInfo").html("");
    $("#productInfo").css("display", "none");
    if (window.innerWidth <= 1250) {
        $("#rightPane").css("position", "unset");
        $("#paneTopBar").css("position", "unset");
    }
}

//add to cart from shop and not preview
function addToCart(product_id) {
    var productCount = 0;
    var cartItem = {};
    console.log(Cart);
    product_exist = false;
    //if the cart is empty add the new product
    if (Cart.length == 0) {
        cartItem = {
            "id": product_id,
            "quantity": 1
        };
        Cart.push(cartItem);
        localStorage.setItem("Cart", JSON.stringify(Cart));
        product_exist = true;
    }
    //if the cart is not empty and the product is already added increase the quantity
    else {
        for (var x = 0; x < Cart.length; x++) {
            if (Cart[x].id == product_id) {
                productCount = JSON.parse(Cart[x].quantity) + 1;
                Cart.splice(x, 1);
                console.log(productCount);
                cartItem = {
                    "id": product_id,
                    "quantity": productCount
                };
                Cart.push(cartItem);
                localStorage.setItem("Cart", JSON.stringify(Cart));
                alert("Quantity has been updated to " + productCount);
                product_exist = true;
            }
        }
    }

    //in the event that the product is not in the cart and the cart is not empty
    if (product_exist == false) {
        cartItem = {
            "id": product_id,
            "quantity": 1
        };
        Cart.push(cartItem);
        localStorage.setItem("Cart", JSON.stringify(Cart));
        product_exist = true;
    }

    console.log(cartItem);
    // Cart.push(product_id);
    $("#Count").html("");
    $("#Count").html(Cart.length);
    //localStorage.setItem("Cart", JSON.stringify(Cart));
    $("#" + product_id + "Button").html("");
    $("#" + product_id + "Button").html("Product added to cart");
    $("#" + product_id + "Button").css("background", "#4caf50");
}


function DisplayCart() {
    $("#products").html("");
    console.log(Cart.length);
    $("#menu").html("");
    $("#menu").html("<li id='cartPrompt'>Your shopping cart</li>");
    if (Cart.length == 0) {
        $("#products").html("<p id='noProducts'>You don't have any products in your cart</p>");
        $("#rightPane").css("height", "100%");
    } else {
        getCartProducts(JSON.parse(localStorage.getItem("Cart")));
    }
}

//render the persons cart
function renderCart(data) {
    $("#products").append("<table><tr><th>Product</th> <th>Price</th> <th>Quantity</th> <th>Remove</th> </tr></table>");
    var total_price = 0;
    for (var x = 0; x < data.length; x++) {
        $("#products").append("<table id='productTable'><tr><td><img width='30' src='http://res.cloudinary.com/jalome/image/upload/c_fill,h_240,w_240/" + data[x].Image + "'/><br id='tableBreak'><span id='cartProductName'>" + data[x].Name + "</span></td> <td><span class='unitPrice' id='" + data[x].id + "unitPrice'>Unit price: R" + data[x].Price + "</span><br id='tableBreak'><span id='" + data[x].id + "cartProductPrice'>total: R" + (data[x].Price * data[x].Quantity) + "</span></td> <td><input type='number' min='0' id='" + data[x].id + "cartQuantityInput' placeholder='" + data[x].Quantity + "'><br id='tableBreak'><span id='cartUpdate' onclick='updateProduct(" + data[x].id + ")'>Update</span><td><span id='removeItem' onclick='removeCartItem(" + data[x].id + ")'>Remove</span></td> </tr></table>");
        total_price += (data[x].Price * data[x].Quantity);
    }

    $("#products").append("<div id='cartBottomSec'><button id='continueBtn' onclick='getProducts()''>Continue shopping</button>  <button id='checkoutBtn' onclick='checkout()'>Proceed to checkout</button> <h1 id='subTotal'>Subtotal: R" + total_price + "</h1></div>");
    console.log(total_price);
}

function checkout() {
    document.location = '/account';
}

function renderAccount(data) {
    if (data.street) {
        $("#id_street").val(data.street);
        $("#id_city").val(data.city);
        $("#id_Province").val(data.province);
        $("#id_Country").val(data.country);
        $("#id_apartment").val(data.apartment);
        $("#id_name").val(data.name);
        $("#id_surname").val(data.surname);
        $("#id_email").val(data.email);
        $("#id_username").val(data.username);
    } else {
        $("#id_username").val(data.username);
        $("#id_email").val(data.email);
        $("#id_name").val(data.name);
        $("#id_surname").val(data.surname);
    }

    if (data.totalPrice > 0) {
        $("#orderCost").html("");
        $("#orderCost").html("R" + data.totalPrice);
        $("#productsCount").html("");
        $("#productsCount").html(data.productcount);
        localStorage.setItem("totalCost", data.totalPrice);
    } else {
        $("#order").css("opacity", "0.5");
        $("#order").css("pointer-events", "none");
    }
}

//when shipping is applied
function applyShipping() {
    var courierGuy = document.getElementById("courierGuyInput");
    var pickup = document.getElementById("localPickupInput");
    var bool = false;
    if (courierGuy.checked == true && $("#orderShipping").html() == "R0") {
        $("#orderShipping").html("");
        $("#orderShipping").html("R75");
        $("#confirmOrder").css("opacity", "1");
        $("#confirmOrder").css("pointer-events", "all");
        var total_cost = JSON.parse($("#orderCost").html().substring(1));
        if (total_cost >= 1800) {
            total_cost = total_cost;
            $("#orderShipping").html("");
            $("#orderShipping").html("Free");
        } else {
            total_cost += 75;
        }

        $("#orderCost").html("");
        $("#orderCost").html("R" + total_cost);
        document.getElementById("localPickupInput").checked = false;
    } else if (courierGuy.checked == false && pickup.checked == false) {
        $("#orderShipping").html("");
        $("#orderShipping").html("R0");
        $("#orderCost").html("");
        $("#orderCost").html("R" + localStorage.getItem("totalCost"));
        $("#confirmOrder").css("opacity", "0.5");
        $("#confirmOrder").css("pointer-events", "none");
    } else {
        document.getElementById("localPickupInput").checked = true;
        document.getElementById("courierGuyInput").checked = false;
        $("#orderShipping").html("");
        $("#orderShipping").html("R0");
        $("#orderCost").html("");
        $("#orderCost").html("R" + localStorage.getItem("totalCost"));
        $("#confirmOrder").css("opacity", "1");
        $("#confirmOrder").css("pointer-events", "all");
    }
}

//order
function order() {
    var cart = JSON.parse(localStorage.getItem("Cart"));
    var shipping = $("#orderShipping").html();
    var totalCost = $("#orderCost").html();
    placeOrder(cart, shipping, totalCost);
}


//update the product depending on how many quantities are selected
//cool ass function
function updateProduct(id) {
    var current_price = JSON.parse($("#" + id + "unitPrice").html().substring(13));
    var current_total = JSON.parse($("#subTotal").html().substring(11));
    var current_total_unit_price = JSON.parse($("#" + id + "cartProductPrice").html().substring(8));
    console.log(current_total_unit_price);
    var num_of_products = document.getElementById(id + "cartQuantityInput").value;
    //if the number of products has not been updated
    if (num_of_products == "" || num_of_products < 1 || num_of_products.includes(".")) {
        num_of_products = 1;

    }
    console.log("Product price is " + current_price);
    console.log("Current total is " + current_total);
    console.log("No of products selected " + num_of_products);
    //remove the unit price from the subtotal
    current_total = current_total - current_price;
    var new_price = current_price * num_of_products;
    //deduct the total cost of the product from the subtotal
    if (current_total_unit_price > current_price) {
        current_total = current_total - current_total_unit_price;
        //add back the unit price to the subtotal
        current_total = current_total + current_price;
    }
    console.log("new price for products " + new_price);
    current_total = current_total + new_price;
    $("#" + id + "cartProductPrice").html("");
    $("#" + id + "cartProductPrice").html("total: R" + new_price);
    $("#subTotal").html("");
    $("#subTotal").html("Subtotal: R" + current_total);

    //update the quantity in the existing cart
    for (var k = 0; k < Cart.length; k++) {
        if (Cart[k].id == id) {
            productCount = num_of_products;
            Cart.splice(k, 1);
            console.log(productCount);
            cartItem = {
                "id": id,
                "quantity": productCount
            };
            Cart.push(cartItem);
            localStorage.setItem("Cart", JSON.stringify(Cart));
            alert("Quantity has been updated to " + productCount);
        }
    }

}

//remove an item from the shopping cart
function removeCartItem(id) {
    var index = Cart.indexOf(id);
    Cart.splice(index, 1);
    console.log(Cart);
    localStorage.setItem("Cart", JSON.stringify(Cart));
    //substract 1 from the cart count
    $("#Count").html("");
    $("#Count").html(JSON.parse(localStorage.getItem("Cart")).length);
    DisplayCart();
}


//create registration form
function registerForm() {
    $("#loginDiv").html("");
    $("#loginDiv").css("height","450px");
    var formError = "<p id='formError'></p>";
    var title = "<h1 id='loginHeading' style='margin-top:0px;'>Create an account</h1>";
    var username = "<p id='loginFormText'>Username*:</p>";
    var username_input = "<input type='text' id='id_username'>";
    var email = "<p id='loginFormText'>Email address*:</p>";
    var email_input = "<input type='email' id='id_email'>";
    var password = "<p id='loginFormText'>Password*:</p>";
    var password_input = "<input type='password' id='id_password'>";
    var register = "<button  id='loginBtn' onclick='registerAccount()'>Register</button>";
    $("#loginDiv").append(formError,title, username, username_input, email, email_input, password, password_input, register, "<span id='loginFormText' onclick='link(" + JSON.stringify('login') + ")'><u>Back</u></span>");
}

function registerAccount() {
    var username = document.getElementById("id_username").value;
    var email = document.getElementById("id_email").value;
    var password = document.getElementById("id_password").value;
    if (username == "" || email == "" || password == "") {
        alert("Please fill in all empty fields");
    } else {
        createAccount(username, email, password);
    }
}


//menu functions
function PlasticFree() {
    $("#overlay").show();
    $("#contentBox").show();
    $("#contentBox").append("<h1>Our plastic free range</h1>");
    $("#contentBox").append("<p style='text-align:justified;'>We at i am SOAP have started taking steps to be plastic free by the end of 2019, our first steps are the plastic free Solid Bars of Shampoo and Conditioner, all they have is a paper card that can be turned into compost, all our bars of soap are <b>PLASTIC FREE</b>, no single use, plastic wrapper or any plastic for that matter. Our Pure Liquid Soap and all our lotions and creams will be available as a refill product in 2019</p>");
    $("#contentBox").append("<img src='/static/website/palstic free.jpg'>");
    $("#contentBox").append("<img src='/static/website/plastic free2.jpg'>");
    $("#contentBox").append("<img src='/static/website/plastic free3.jpg'>");
    $("#contentBox").append("<img src='/static/website/plastic free4.jpg'>");
    $("#contentBox").append("<p style='margin-top:20px; float:left'>Plastic free shampoo bars</p>");
    Mobilemenu();
}

//
function closeOverlay() {
    $("#overlay").hide();
    $("#contentBox").hide();
    $("#contentBox").html("");
}

function link(link) {
    document.location = link;
}


function Registerlink() {
    document.location = "/register";
}

//view stockists
function stores(){ 
    document.location = '/stockists';
 }

//menu display/close
function Mobilemenu() {
    var menuIcon = document.getElementById("menuIcon");
    var srcAttr = menuIcon.getAttribute("src");

    if (srcAttr == "/static/website/menu.svg") {
        menuIcon.setAttribute("src", "/static/website/cancel.svg");
        $("#leftPane").css("height", "400px");
        //add rotation 
        $("#menuIcon").addClass("animated rotateIn").one("webkitAnimationEnd", function () {
            $("#menuIcon").removeClass();
        });
        $("#leftPane").addClass("menuExtend").one('webkitAnimationEnd', function () {
            $("#leftPane").removeClass();
            $("#leftPane").append(
                "<p class='menuList' style='margin-top:50px;' onclick='document.location =" + JSON.stringify('/') + "'>Home</p><p class='menuList' onclick='getProducts()'>Shop</p><p class='menuList' onclick='document.location =" + JSON.stringify('/account') + "'>Account</p><p class='menuList' onclick='PlasticFree()'>Plastic free</p><p class='menuList' onclick='stores()'>Stockists</p><!--<p class='menuList'>White labels</p><p class='menuList'>FAQ</p>--><p class='menuList' onclick='contact()'>Contact</p>"
            );
        });
        //
    } else {
        menuIcon.setAttribute("src", "/static/website/menu.svg");
        var menuLists = $(".menuList");
        console.log(menuLists);
        for (var x = 0; x < menuLists.length; x++) {
            menuLists[x].style.display = 'none';
        }
        $("#leftPane").css("height", "50px");
        $("#menuIcon").addClass("animated rotateIn").one("webkitAnimationEnd", function () {
            $("#menuIcon").removeClass();
        });
        $("#leftPane").addClass("menuUnExtend").one('webkitAnimationEnd', function () {
            $("#leftPane").removeClass();
        });
    }

}


function renderSearchResults(data){
    $("#rightPane").html("");
    $("#rightPane").append("<div id='productInfo'></div>");
    var pane = $("#rightPane");
    var paneTopBar = $("<div id='paneTopBar'><p id='searchResultsText'>"+data.length+" Search results</p></div><br><br><br>");
    pane.append(paneTopBar);
    for(var o = 0; o < data.length; o++){
        image_link = data[o].image;
        price = data[o].price;
        name = data[o].name;
        Category  = data[o].category;
        id = data[o].id;
        productTab = $("<div id='productTab'><img src='http://res.cloudinary.com/jalome/image/upload/c_fill,h_240,w_240/" + image_link + "'/> <p id='name'>" + name + "</p><p id='category'>" + Category + "</p><p id='price'>R" + price + "</p> <button onclick='displayImg("+id+")'>View product</button></div>");
        $("#rightPane").append(productTab);
    }
}


//contact form pop up
function contact(){
    $("#rightPane").html("");
    var pane = $("#rightPane");
    var paneTopBar = $("<div id='paneTopBar'><p id='searchResultsText'>Contact I am SOAP</p></div><br id='contactWebBreak'><br id='contactWebBreak'><br id='contactWebBreak'>");
    var contactBox = $("<div id='contactBox'></div>");
    var Footer = $("<footer><div id='author'><p>Website developed by Jalome Chirwa</p></div><div id='socialIcon'><span>Social media links:</span><a href='https://www.instagram.com/i_am_soap/' target='_blank'><i class='fa fa-instagram'></i></a><a href='https://twitter.com/i_am_SOAP_ZA' target='_blank'><i class='fa fa-twitter'></i></a><i class='fa fa-facebook'></i></div></footer>");
    var formBox = $("<div id='formBox'><div id='contactFormDiv1'><input id='nameContact' type='text' Placeholder='Your name*'><br i='contactBreak'><input type='email' Placeholder='Your email address*' id='emailContact'></div> <div id='contactBoxDiv2'><input type='text' id='contactNum' Placeholder='Your mobile number*'><br i='contactBreak'><select id='messageTo'><option disabled selected>Message to</option><option>Customer support</option><option>Web developer</option></select></div> <div id='contactDiv3'><textarea placeholder='Message*' id='contactMessage'></textarea></div> <button id='contactSubmit' onclick='sendMessage()'>Send message</button></div>");
    var InfoBox = $("<div id='infoBox'><br><h1>Our address:</h1><p>18 Opstal Rd, Terenure, Kempton Park, 1619</p> <h1>Email address:</h1><p>neil@iamsoap.co.za</p> <h1>Mobile number:</h1><p>083 444 8699</p> <h1>Operating hours</h1><p>Mon - Thurs: 09am - 4:30pm</p><p>Fri: 09am - 1:30pm</p><p>Closed on Sat,Sun and public holidays</p><p>Open 24/7 online</p></div>");
    contactBox.append(formBox, InfoBox);
    pane.append(paneTopBar, contactBox, Footer);
    if(window.innerWidth < 1250){
        Mobilemenu();
    }

}

//
function sendMessage(){
    var name = $("#nameContact").val();
    var email = $("#emailContact").val();
    var mobile = $("#contactNum").val();
    var to = $("#messageTo").val();
    var message = $("#contactMessage").val();
    if(name == "" || email == "" || mobile == "" || to == null || message == ""){
        alert("Please fill in all the required fields");
    }else{
        contactFormMessage(name,email,mobile,to,message);
    }
}

//result of send message from the contact form
function renderContactMessageResult(message){
    $("#rightPane").html("");
    $("#rightPane").html("<p id='contactFormMessage'>"+message+"</p>");
}

//export table
var tableToExcel = (function() {
    var uri = 'data:application/vnd.ms-excel;base64,'
      , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
      , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
      , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
    return function(table, name) {
      if (!table.nodeType) table = document.getElementById(table)
      var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
      window.location.href = uri + base64(format(template, ctx))
    }
  })()


//call the function to shuffle your array, pass your array as a parameter and will
//be returned as a reshuffled array e.g var array = shuffleArray(["1", "2", "3", "4"]);
function shuffleArray(array) {
    tempArray = [];
    while (tempArray.length != array.length) {
        for (var i = 0; i < array.length; i++) {
            var randomNo = Math.floor(Math.random() * (array.length));
            console.log("random number is " + randomNo);
            var arrayText = array[randomNo];
            if (tempArray.includes(arrayText)) {} else {
                tempArray.push(arrayText);
            }
        }

        console.log(tempArray);
    }

    return tempArray;
}
