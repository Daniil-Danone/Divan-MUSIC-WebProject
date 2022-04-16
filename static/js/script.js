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

$('.registration__form__start').find('.custom__input__field').attr('autocomplete', 'off');

$(document).ready(function () {
    let pattern = /^[a-z0-9_-]+@[a-z0-9-]+\.([a-z]{1,6}\.)?[a-z]{2,6}$/i
    let password_pattern = /^[a-z0-9_-]$/
    let input = $('.custom__input__field')


    input.on('change keyup', function () {
        if ($(this).val() !== '') {
            if ($(this).attr('id') === 'email') {
                if (checkEmail($(this).val()) === true) {successField($(this))}
                else {errorField($(this), 'Почта введена неверно!')}
            }

            if ($(this).attr('id') === 'password') {
                if (checkPassword($(this).val()) === true) {successField($(this))}
                else {errorField($(this), 'Пароль слишком короткий (минимум 4 символа)!')}
            }

            if ($(this).attr('id') === 'username') {
                if (eel.check_username(value) === true) {errorField($(this), 'Пользователь уже существует!')}
                else {successField($(this))}
            }
        }
        else {emptyField($(this))}

        $(this).parents('.reg__field__grid').find("#form__continue").click(function () {
            $(this).parents('.reg__from__elem').addClass('active')
        })
    })


    function checkEmail(email) {
        if (email !== '') {
            return email.search(pattern) === 0;
        } else {
            return false
        }
    }

    function checkPassword(password) {
        return !!(password.length >= 4 && password.search(password_pattern));
    }

    function successField(field) {
        field.parents('.reg__field__grid').find("#status").text('Отлично!')
            .removeClass('field__error').addClass('field__success');
        field.parents('.reg__field__grid').find("#form__continue").attr('disabled', false)
            .removeClass('disabled');
        field.removeClass('field__error').addClass('field__success');

        field.parents('.reg__field__grid').find("#form__continue").click(function () {
            $(this).parents('.reg__field__grid').find('#success__img').removeClass('hide');
            $(this).parents('.reg__field__grid').find("#form__continue").addClass('hide')
        });
    }

    function errorField(field, error) {
        field.parents('.reg__field__grid').find('#success__img').addClass('hide');
        field.parents('.reg__field__grid').find("#form__continue").attr('disabled', true)
            .addClass('disabled').removeClass('hide');
        field.parents('.reg__field__grid').find("#status").text(error)
            .removeClass('field__success').addClass('field__error');
        field.removeClass('field__success').addClass('field__error');
    }

    function emptyField(field) {
        field.parents('.reg__field__grid').find('#success__img').addClass('hide');
        field.parents('.reg__field__grid').find("#form__continue").attr('disabled', true)
            .addClass('disabled').removeClass('hide');
        field.parents('.reg__field__grid').find("#status").text('Поле не должно быть пустым')
            .removeClass('field__success').addClass('field__error');
        field.removeClass('field__success').addClass('field__error');
    }

    function checkUsername(value) {
        async function send () {
            await eel.check_username(value);
            if (eel.check_username(value) === true) {
                return true
            }else {
                return false
            }
        }
    }
})