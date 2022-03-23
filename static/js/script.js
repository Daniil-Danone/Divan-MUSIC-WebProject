$(document).ready(function () {
    $('.header__burger').click(function(event) {
        $('.header__burger,.header__menu').toggleClass('active')
        $('body').toggleClass('lock')
    });

    $('.custom__checkbox').click(function(event) {
        $('.custom__checkbox').toggleClass('active')
    });

    $(document).on('click', '.custom__radio__button__item', function(event) {
        $(this).parents('.custom__radio__buttons').find('.custom__radio__button__item').removeClass('active');
        $(this).parents('.custom__radio__buttons').find('.custom__radio__button__item input').prop('checked', false);
        $(this).toggleClass('active');
        $(this).find('input').prop('checked', true);
        return false
        }

    )
});