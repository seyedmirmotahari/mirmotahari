// Smooth scrolling for navigation links
$(document).ready(function() {
    // Smooth scroll for all anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        var target = $(this.getAttribute('href'));
        
        if(target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Active navigation highlighting
    $(window).on('scroll', function() {
        var scrollPos = $(window).scrollTop();
        
        $('.nav-links a').each(function() {
            var currLink = $(this);
            var refElement = $(currLink.attr('href'));
            
            if (refElement.length) {
                if (refElement.offset().top - 100 <= scrollPos && 
                    refElement.offset().top + refElement.height() > scrollPos) {
                    $('.nav-links a').removeClass('active');
                    currLink.addClass('active');
                } else {
                    currLink.removeClass('active');
                }
            }
        });

        // Add shadow to nav on scroll
        if (scrollPos > 50) {
            $('#main-nav').css('box-shadow', '0 2px 20px rgba(0, 0, 0, 0.1)');
        } else {
            $('#main-nav').css('box-shadow', '0 2px 10px rgba(0, 0, 0, 0.1)');
        }
    });

    // Fade in elements on scroll
    function fadeInOnScroll() {
        $('.portfolio-item').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).css('opacity', '1');
                $(this).css('transform', 'translateY(0)');
            }
        });
    }

    // Initial state for fade-in elements
    $('.portfolio-item').css({
        'opacity': '0',
        'transform': 'translateY(30px)',
        'transition': 'all 0.6s ease'
    });

    // Trigger fade-in on scroll
    $(window).on('scroll', fadeInOnScroll);
    fadeInOnScroll(); // Initial check

    // Mobile menu toggle (if needed)
    $('.mobile-menu-toggle').on('click', function() {
        $('.nav-links').toggleClass('show');
    });
});
