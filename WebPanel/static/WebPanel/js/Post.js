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
        '<div class="mdl-card mdl-shadow--4dp mdl-cell mdl-cell--12-col">' +
            '<div class="mdl-card__title mdl-color-text--grey-50">' + 
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
            '<div class="mdl-color-text--primary-contrast mdl-card__supporting-text post-comments">' +
                '<form id="form_comment">' +
                    '<div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">' +
                        '<textarea id="id_comment-content" name="comment-content" rows="1" class="mdl-textfield__input"></textarea>' +
                        '<label for="id_comment-content" class="mdl-textfield__label">Join the conversation</label>' +
                    '</div>' +
                    '<button class="mdl-button mdl-js-button mdl-button--icon"><i class="material-icons">check</i></button>' +
                '</form>' +
                '<div id="div_commentTable"></div>' +
            '</div>' +
        '</div>';
    $('#div_postDetail').html(div_post);
    get_next_page()
}

function get_comment_like_button(id, active, replies) {
    var button_style = (active) ? ' style="color: #00796b"' : '';
    return '<i class="material-icons" onclick="post_commentInteraction(' + id + ',' + 'true' + ', ' + replies + ')"' + button_style + '>thumb_up</i>'
}

function get_comment_dislike_button(id, active, replies) {
    var button_style = (active) ? ' style="color: #00796b"' : ''
    return '<i class="material-icons" onclick="post_commentInteraction(' + id + ',' + 'false' + ', ' + replies + ')"' + button_style + '>thumb_down</i>'
}

function draw_comment_replies(comment) {
    console.log(comment.replies);
    var div = '<div id="replies_' + comment.id + '" class="comment__replies">';
    for (var i=0; i<comment.replies.length; i++) {
        div += ('<div id="comment_' + comment.replies[i].id + '">' + draw_comment(comment.replies[i], false) + '</div>')
    }
    return div + '</div>'
}

function draw_comment(comment, replies) {
    var div_comment = '' +
        '<div class="comment mdl-color-text--grey-700">' +
            '<header class="comment__header">' +
                '<img src="' + ((comment.author.avatar) ? comment.author.avatar : icon_profileDark) + '" class="comment__avatar">' +
                '<div class="comment__author">' +
                    '<strong>' + escapeHtml(comment.author.display) + '</strong>' +
                '</div>' +
            '</header>' + 
            '<div class="comment__text">' + escapeHtml(comment.content) + '</div>' +
            '<nav class="comment__actions">' +
                get_comment_like_button(comment.id, comment.liked, replies) +
                get_comment_dislike_button(comment.id, comment.disliked, replies) +
                comment.points + ' points' +
            '</nav>' + 
            ((replies) ? draw_comment_replies(comment) : '') +
        '</div>';
    return div_comment;
}

function load_comments(comments) {
    for (var i=0; i<comments.length; i++) {
        var comment = '' + 
            '<div id="comment_' + comments[i].id + '">' +
                draw_comment(comments[i], true) +
            '</div>';
        $('#div_commentTable').append(comment);
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
                    load_comments(data.results);
                }
                block_nextPage = false;
            },
            error: function () { block_nextPage = false; }
        })
    }
}

function no_more_results() { $('#div_commentMessage').show(); }

function post_interaction(id, like) {
    if (!authenticated) { show_login(); return }
    $.ajax({
        url: url_postInteraction.replace('/0/', '/'+id+'/').replace('like', (like) ? 'like' : 'dislike'),
        method: 'POST',
        dataType: 'json',
        success: function (data) { posted_postInteraction(data) }
    })
}

function posted_postInteraction(post) {
    $('#post-bar_' + post.id).html(draw_post_bar_actions(post))
}

function post_commentInteraction(id, like, replies) {
    if (!authenticated) { show_login(); return }
    $.ajax({
        url: url_postCommentInteraction.replace('/0/', '/'+id+'/').replace('like', ((like) ? 'like' : 'dislike')),
        method: 'POST',
        dataType: 'json',
        success: function (data) { $('#comment_' + id).html(draw_comment(data, replies)) }
    })
}

function post_comment() {
    if (!authenticated) { show_login(); return }
    $.ajax({
        url: url_postCommentList,
        method: 'POST',
        data: $('#form_comment').serialize(),
        dataType: 'json',
        success: function (data) { posted_comment(data); },
        error: function () { show_post_error() }
    })
}

function posted_comment(comment) {
    var current = $('#div_commentTable').html();
    $('#div_commentTable').html(draw_comment(comment) + current);
    $('#form_comment input').val('');
}