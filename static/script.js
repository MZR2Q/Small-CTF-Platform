document.getElementById('disabledButton').addEventListener('click', function() {
    alert('UHBFlag{?_JS_IMPORT_?_FOX_?}');
});


function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;


    var expectedUsername = 'Admin';
    var expectedPassword = 'admin11221122';

    if (username === expectedUsername && password === expectedPassword) {
        alert('Welcome, ' + username + '!');
    } else {
        alert('Incorrect username or password. Please try again. Check js code ????');
    }
}


// UHBFlag{?__js_IMPORT_?_?_?__} //