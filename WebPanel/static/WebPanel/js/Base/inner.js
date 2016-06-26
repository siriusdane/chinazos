// HTML ESCAPING UTILITY
var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': '&quot;',
    "'": '&#39;',
    "/": '&#x2F;'
};

function escapeHtml(string) {
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}

// CSRF
var csrftoken = Cookies.get('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
});

// Login Dialog
var dialog_login = document.querySelector('#dialog_login');
if (! dialog_login.showModal) { dialogPolyfill.registerDialog(dialog_login); }
dialog_login.querySelector('.close').addEventListener('click', function() {
    dialog_login.close();
});

// Register Dialog
var dialog_register = document.querySelector('#dialog_register');
if (! dialog_register.showModal) { dialogPolyfill.registerDialog(dialog_register); }
dialog_register.querySelector('.close').addEventListener('click', function() {
    dialog_register.close();
});

function login() {
    $.ajax({
        url: url_loginService,
        method: 'POST',
        data: $('#form_login').serialize(),
        dataType: 'text',
        success: function () { location.reload() },
        error: function () { show_login_error() }
    })
}

function logout() {
    $.ajax({
        url: url_logoutService,
        method: 'POST',
        dataType: 'text',
        success: function () { location.reload() }
    })
}

function register() {
    $.ajax({
        url: url_registerService,
        method: 'POST',
        data: $('#form_register').serialize(),
        dataType: 'text',
        success: function () { location.reload() },
        error: function () { show_register_error() }
    })
}

function show_login() {
    $('#form_login input').val('');
    $('#span_loginError').css('visibility', 'hidden');
    dialog_login.showModal();
}

function show_register() {
    $('#form_register input').val('');
    $('#span_registerError').css('visibility', 'hidden');
    dialog_register.showModal();
}

function show_login_error() {
    $('#span_loginError').css('visibility', 'visible');
}

function show_register_error() {
    $('#span_registerError').css('visibility', 'visible');
}

function gotoHome() {
    location.href = url_home;
}