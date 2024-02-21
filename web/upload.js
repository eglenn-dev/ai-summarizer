let form = document.querySelector('form');
let output = document.querySelector('.output');

form.onsubmit = async (ev) => {
    ev.preventDefault();
    output.textContent = 'Summarizing, please wait...';

    var fileInput = document.getElementById('pdfInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);
    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(function (response) {
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        return response.text();
    }).then(function (text) {
        document.getElementById('output').textContent = text;
    }).catch(function (error) {
        document.getElementById('output').textContent = error.message;
    });
};