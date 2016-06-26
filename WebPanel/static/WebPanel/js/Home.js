var block_nextPage = false;

// Post Dialog
var dialog_post = document.querySelector('#dialog_post');
if (! dialog_post.showModal) { dialogPolyfill.registerDialog(dialog_post); }
dialog_post.querySelector('.close').addEventListener('click', function() {
    dialog_post.close();
});

function show_post() {
    $('#form_post input').val('');
    $('#span_postError').css('visibility', 'hidden');
    dialog_post.showModal();
}

function show_post_error() {
    $('#span_postError').css('visibility', 'visible');
}

function gotoPost(id) {
    location.href = url_postDetail.replace('/0/', '/'+id+'/');
}

function get_like_button(id, active) {
    var button_style = (active) ? ' style="color: #00796b"' : '';
    return '<i class="material-icons" onclick="post_interaction(' + id + ',' + 'true' + ')"' + button_style + '>thumb_up</i>'
}

function get_dislike_button(id, active) {
    var button_style = (active) ? ' style="color: #00796b"' : ''
    return '<i class="material-icons" onclick="post_interaction(' + id + ',' + 'false' + ')"' + button_style + '>thumb_down</i>'
}

function draw_post_bar_actions(post) {
    var post_bar = '' +
        '<div class="post-bar__actions">' +
            get_like_button(post.id, post.liked) +
            get_dislike_button(post.id, post.disliked) +
            '<span>' + post.points + ' points</span>' +
        '</div>';
    return post_bar
}

function draw_post(post) {
    var div_post = '' +
        '<div class="mdl-card mdl-shadow--4dp mdl-cell mdl-cell--6-col">' +
            '<div class="mdl-card__title mdl-color-text--grey-50" onclick="gotoPost(' + post.id + ')">' + 
                '<h3 class="quote">' + escapeHtml(post.content) + '</h3>' +
            '</div>' +
            '<div class="mdl-card__title mdl-color-text--grey-50">' + 
                '<div class="mdl-layout-spacer"></div>' +
                '<span>' + escapeHtml(post.title) + '</span>' +
            '</div>' +
            '<div class="mdl-color-text--grey-700 mdl-card__supporting-text post-bar">' +
                '<img src="' + ((post.author.avatar) ? post.author.avatar : icon_profileDark) + '">' +
                '<span>' + escapeHtml(post.author.display) + '</span>' +
                '<div class="section-spacer"></div>' +
                '<div id="post-bar_' + post.id + '">' +
                    draw_post_bar_actions(post) +
                '</div>' +
            '</div>' +
        '</div>';
    return div_post;
}

function load_posts(posts) {
    for (var i=0; i<posts.length; i++) {
        var post = '<div id="post_' + posts[i].id + '">' + draw_post(posts[i]) + '</div>';
        $('#div_postTable').append(post);
    }
}

function get_next_page() {
    if (url_nextPage == null) { no_more_results() }
    else if (!block_nextPage) {
        block_nextPage = true;
        $.ajax({
            url: url_nextPage,
            method: 'GET',
            dataType: 'json',
            success: function (data) {
                if (data.results.length == 0) { no_more_results() }
                else {
                    url_nextPage = data.next;
                    load_posts(data.results);
                }
                block_nextPage = false;
            },
            error: function () { block_nextPage = false; }
        })
    }
}

function no_more_results() { $('#div_postMessage').show(); }

function post_interaction(id, like) {
    if (!authenticated) { show_login(); return }
    $.ajax({
        url: url_postInteraction.replace('/0/', '/'+id+'/').replace('like', ((like) ? 'like' : 'dislike')),
        method: 'POST',
        dataType: 'json',
        success: function (data) { $('#post-bar_' + id).html(draw_post_bar_actions(data)) }
    })
}

function post_chinazo() {
    if (!authenticated) { show_login(); return }
    $.ajax({
        url: url_postList,
        method: 'POST',
        data: $('#form_post').serialize(),
        dataType: 'json',
        success: function (data) { posted_chinazo(data) },
        error: function () { show_post_error() }
    })
}

function posted_chinazo(post) {
    var current = $('#div_postTable').html();
    $('#div_postTable').html(draw_post(post) + current);
    dialog_post.close();
}