import { streamGemini } from './gemini-api.js';

let form = document.querySelector('form');
let output = document.querySelector('.output');

form.onsubmit = async (ev) => {
    ev.preventDefault();
    output.textContent = 'Summarizing, please wait...';

    let fileInput = document.getElementById('pdfInput');
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append('file', file);

    // Use fetch to send the FormData to the server
    fetch('/api/doc', {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(text => {
            let md = new markdownit();
            let innterText = md.render(text);
            document.querySelector('.output').innerHTML = innterText;
        })
        .catch(error => {
            document.querySelector('.output').textContent = error.message;
        });
};