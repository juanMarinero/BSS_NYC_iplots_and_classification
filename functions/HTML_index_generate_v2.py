#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :


def HTML_index_generate_v2(IndexId="#table-of-content"):
    """
    MWE:
    from ML_fcns.HTML_index_generate import HTML_index_generate
    from IPython.display import display, Javascript

    display(Javascript(HTML_index_generate()))
    """

    js_code = """
    var toc = '';
    var headers = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    var symbols = ['●', '○', '—', '', '', ''];  // Add symbols here for each level
    var fontSizes = [2, 1.5, 1, 1, 1, 1];      // Define font sizes here for each level

    for (var i = 0; i < headers.length; i++) {
        var header = headers[i];
        var level = parseInt(header.tagName.charAt(1)) - 1;
        var id = header.getAttribute('id');
        var title = header.innerText;
        var symbol = symbols[level];
        var fontSize = fontSizes[level] + 'em';

        if (!id) {
            id = 'header-' + level + '-' + i;
            header.setAttribute('id', id);
        }

        var link = '<a style="font-size: ' + fontSize + '; margin-left: ' + (level * 15) + 'px;" href="#' + id + '">' + symbol + ' ' + title + '</a><br>';
        toc += link;
    }
    """
    js_code += f"document.querySelector('{IndexId}').innerHTML = toc;"

    # Display the TOC using JavaScript
    #  from IPython.display import display, Javascript
    #  display(Javascript(js_code))
    return js_code
