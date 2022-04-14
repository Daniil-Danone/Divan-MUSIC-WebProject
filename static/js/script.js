$(document).ready(function () {
    $('.header__burger').click(function() {
        $('.header__burger,.header__menu').toggleClass('active');
        $('body').toggleClass('lock');
    });

    $('.custom__checkbox.accept__checkbox').click(function() {
        $('.custom__checkbox.accept__checkbox').toggleClass('active');
        $(this).find('input').prop('checked', true);
    });

    $('.custom__checkbox.remember_me').click(function() {
        $('.custom__checkbox.remember_me').toggleClass('active');
    });

    $(document).on('click', '.custom__radio__button__item', function() {
        $(this).parents('.custom__radio__buttons').find('.custom__radio__button__item').removeClass('active');
        $(this).parents('.custom__radio__buttons').find('.custom__radio__button__item input').prop('checked', false);
        $(this).toggleClass('active');
        $(this).find('input').prop('checked', true);
        return false
    });
});

$('.registration__form__start').find('input').attr('autocomplete', 'off');

$(document).ready(function(){
    $(".registration__form__start").validate({
        rules:{
            email:{
                required: true,
                minlength: 4,
            },
        },
        messages:{
            email:{
                email: 'Неверный почтовый адрес',
                required: "Это поле обязательно для заполнения",
                minlength: "Логин должен быть минимум 4 символа",
                maxlength: "Максимальное число символов - 16",
            },
        },
        submitHandler: function() {
            $('.custom__input__field').toggleClass('success');
        }
    });
});