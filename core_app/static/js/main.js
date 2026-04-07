document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.msg[data-dismiss]');
    alerts.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.4s';
            el.style.opacity = '0';
            setTimeout(function () { if (el.parentNode) el.remove(); }, 400);
        }, 4000);
    });

    var readBar = document.querySelector('.mobile-price-bar');
    if (readBar) {
        document.body.classList.add('has-read-bar');
    }

    var animatedCards = document.querySelectorAll(
        '.vip-card-wrapper, .ad-card, .related-card, .search-card, .auth-card, .profile-ad-item, .ad-form-card, .delete-card, .price-box'
    );
    animatedCards.forEach(function (el) {
        el.classList.add('reveal-on-scroll');
    });

    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reducedMotion && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries, obs) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

        animatedCards.forEach(function (el) {
            observer.observe(el);
        });
    } else {
        animatedCards.forEach(function (el) {
            el.classList.add('is-visible');
        });
    }
});
