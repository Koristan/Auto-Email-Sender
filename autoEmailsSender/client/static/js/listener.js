$(document).ready(function () {

    // Listeners

    // Create Template
    $('#create-form .btn.create').on('click', function (e) {

        e.preventDefault();
        let form = $(this).closest('#create-form');

        let template_name = form.find('input[name=template_name]').val();
        let file = form.find('input[name=template_file]').prop('files')[0];
        let formdata = new FormData();
        formdata.append('template_name', template_name);
        formdata.append('template_file', file)
        if (template_name == '') {
            alert('Заполните название шаблона');
            return;
        } else if (template_name.includes('.') || template_name.includes(',') || template_name.includes('/') || template_name.includes('\\') || template_name.includes(' ')) {
            alert("В шаблоне не должно быть точек, запятых, пробелов и других специальных символов");
            return;
        } else if (form.find('input[name=template_file]').get(0).files.length === 0) {
            alert('Файл пустой!');
            return;
        }

        $.ajax({
            url: '/api/templates/create',
            method: 'post',
            data: formdata,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (typeof data['err'] !== 'undefined') {
                    alert(data['err']);
                }
                else {
                    alert(data['msg']);
                }
                $('input').val('');
            }
        });
    });

    // Delete Template
    $('#create-form .btn.delete').on('click', function (e) {

        e.preventDefault();
        let form = $(this).closest('#create-form');

        let formdata = new FormData();
        formdata.append('template_name', form.find('input[name=template_name]').val());
        $.ajax({
            url: '/api/templates/delete',
            method: 'post',
            data: formdata,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (typeof data['err'] !== 'undefined') {
                    alert(data['err']);
                }
                else {
                    alert(data['msg']);
                }
            }
        });
    });

    // Load Templates List
    if (location.pathname == '/send') {

        $.ajax({
            url: '/api/templates/get',
            method: 'post',
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (typeof data['err'] !== 'undefined') {
                    alert(data['err']);
                }
                else {
                    let wrapper = $('#template');
                    first = 'selected';
                    data.msg.forEach(element => {
                        wrapper.append('<option value="' + element + '">' + element + '</option>');
                    });
                }
            }
        });

    }

    $('#send-form .append').on('click', function () {
        $('#send-form .fields').append('<div class="field"><input type="text" class="field_to_replace_key" placeholder="Ключ"><input type="text" class="field_to_replace_value" placeholder="Значение"></div>');
    });

    // Get Email Template
    $('#send-form .btn.temp').on('click', function (e) {

        e.preventDefault();
        let form = $(this).closest('#send-form');

        let formdata = new FormData();
        formdata.append('template', form.find('select[name=template]').val());
        formdata.append('addresses', form.find('textarea[name=addresses]').val());
        formdata.append('title', form.find('textarea[name=title]').val());
        formdata.append('fields', JSON.stringify(get_all_fields(form)));

        $.ajax({
            url: '/api/presend',
            method: 'post',
            data: formdata,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (typeof data['err'] !== 'undefined') {
                    alert(data['err']);
                }
                else {
                    $('#template-preview p').html(data.replace(/\n/g, '<br>'));
                    $('#send-form .right-side .send').css('display', 'flex');
                }
            }
        });
    });

    // Send Emails
    $('#send-form .btn.send').on('click', function (e) {

        e.preventDefault();
        let form = $(this).closest('#send-form');
        form.addClass('pause');
        let formdata = new FormData();
        formdata.append('template', form.find('select[name=template]').val());
        formdata.append('addresses', form.find('textarea[name=addresses]').val());
        formdata.append('title', form.find('input[name=title]').val());
        formdata.append('fields', JSON.stringify(get_all_fields(form)));

        $.ajax({
            url: '/api/send',
            method: 'post',
            data: formdata,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                if (typeof data['err'] !== 'undefined') {
                    alert(data['err']);
                }
                else {
                    alert(data['msg']);
                }
                form.removeClass('pause');
            }
        });
    });




    // Load Addresses
    $('#send-form select').on('input', function () {
        load_addresses();
    });

    if (location.pathname == '/send') {
        setTimeout(() => {  load_addresses(); }, 300);
    }

    function load_addresses() {
        let formdata = new FormData();
        formdata.append('template', $('select[name=template]').val());
        
        $.ajax({
            url: '/api/load_addresses',
            method: 'post',
            contentType: false,
            cache: false,
            data: formdata,
            processData: false,
            success: function (data) {
                $('#send-form textarea[name=addresses]').val(data);
            }
        });
    }

    function get_all_fields(form) {
        let fields = [];

        form.find('.field').each(function () {
            let key = $(this).find('.field_to_replace_key').val();
            let value = $(this).find('.field_to_replace_value').val();
            if (key != '' && value != '') {
                fields.push([key, value]);
            }
        });

        return fields;
    }

});
