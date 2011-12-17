kwiki_identifier = 'wiki' + window.location.pathname.replace(/\//g, '_').replace('index.html', '').replace('.html', '');

var kwiki = kwiki || {};

kwiki.getCSS = function(url) {
    var tag = '<link rel="stylesheet" href="' + url + '" />';
    $('body').append(tag);
};

kwiki.insertCSS = function(url) {
    $.get(url, function(res) {
        var tag = '<style>' + res + '</stle>';
        $('body').append(tag);
    });
};

kwiki.insertScript = function(url, bottle) {
    var tag = '<script src=' + url + '></script>';
    if (!bottle) bottle = 'head';
    $(bottle).append(tag);
};

kwiki.loadCmt = function(provider) {
    if ($('#no-comment').length > 0) return;

    var thread, extraCSS, theJS;

    $('#main').append(thread);

    var win = $(window);

    function load() {
        if (win.scrollTop() + win.height() > thread.offset().top - 100) {

            if (extraCSS) kwiki.getCSS(extraCSS);

            $.getScript(theJS);

            win.unbind('scroll');
        }
    }

    win.bind('scroll', load);
    load();
};

$(document).ready(function() {
    if (window.innerWidth >= 460) {
        var toggler = $('<div class="toggler" title="点击展开/收起，Shift+Z 隐藏或打开">目录</div>'),
        toc = $('.toc');
        toc.wrap('<div class="tocWrap">');

        $('.tocWrap').prepend(toggler)
        .delay(500)
        .fadeTo(500, '0.25')
        .hover(function() {
            $(this).stop().fadeTo(300, '0.9');
        }, function() {
            $(this).stop().fadeTo(300, '0.25');
        });

        $('html').keypress(function(e) {
            if (e.shiftKey && (e.charCode || e.keyCode) == '90') {
                e.preventDefault();
                $('div.tocWrap').toggle(200);
            }
        });

        toggler.click(function() {
            $('div.toc').slideToggle(300);
        });
    }

    //外链处理
    $('a[href]').each(function() {
        if (this.href.indexOf(window.location.host) == -1) $(this).attr({target: '_blank', title: this.href });
    });

    $('a[href^=#][href!=#]').click(function() {

        var target = document.getElementById(this.hash.slice(1));

        if (!target) return;

        var targetOffset = $(target).offset().top;
        $('html,body').animate({scrollTop: targetOffset}, 400);

        return false;
    });

    //lesser
    $('div.lesser .hd').click(function() { $(this).next().slideToggle(300); });

    //把< 转为html实体>

  
});

//Google 统计
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-27783960-1']);
_gaq.push(['_trackPageview']);

$.getScript('http://www.google-analytics.com/ga.js');



