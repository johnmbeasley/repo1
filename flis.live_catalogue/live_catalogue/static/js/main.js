$(function () {

    var submitFilterForm = function (e) {
        e.preventDefault();
        $(this).parents('form').submit();
    }

    var catalogue_filter = $('#catalogue-filter');
    catalogue_filter.on('change', 'input[type=radio]', submitFilterForm);

    $('.select').select2({
        width: 'resolve'
    });

    $('.select').each(function () {
        var $this = $(this);
        if($this.data('readonly') == 'readonly') {
            $this.select2('readonly', true);
        }
    });

    $('#document-add').on('click', function () {
        var i = $('#documents-container').find('.document-container-upload').length;
        var max_forms = parseInt($('#id_form-MAX_NUM_FORMS').val());
        if(i >= max_forms - 1) {
            $(this).hide();
        }
        var dc = $('#documents-container')
            .find('.document-container-upload:last')
            .clone();
        var input = dc.find('input')
        input.attr('name', 'form-' + i + '-name');
        input.attr('id', 'id_form-' + i + '-name');
        input.val('');
        $('#id_form-TOTAL_FORMS').val(i+1);
        $('#document-add').before(dc);
    });

    $('.document-container').on('click', '.remove', function (e) {
        e.preventDefault()
        if(!confirm('Are you sure you want to delete this file?')) {
            return;
        }

        var i = $('#documents-container').find('.document-container').length;
        var max_forms = $('#id_form-MAX_NUM_FORMS').val();

        var $this = $(this);
        var href = $this.data('href');
        $.ajax({
            type: 'DELETE',
            url: href,
            success: function (data) {
                $this.parents('.document-container').fadeOut('fast', function () {
                    $(this).remove();
                });
                if(i - 1 <= max_forms) {
                    $('#document-add').show();
                }
            }
        });

    });

    $.fn.dataTable.ext.order['timestamp'] = function  ( settings, col ) {
        return this.api().column( col, {order:'index'} ).nodes().map( function ( td, i ) {
            return $(td).data('timestamp') * 1;
        } );
    }

    $('table[data-toggle=datatable]').dataTable({
        bLengthChange: false,
        aaSorting: [[ 2, 'desc' ]],
        bInfo: false,
        iDisplayLength: 50,
        aoColumnDefs: [
            { "sType": "html", "aTargets": [ 1 ] },
            { "orderDataType": "timestamp", "aTargets": [ 2 ] }
        ],
        sPaginationType: 'bootstrap'
    });


    $('*[data-toggle=popover]').popover({
        trigger: 'hover',
        html: true
    });

});
