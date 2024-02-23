import { streamGemini } from './gemini-api.js';

let form = document.querySelector('form');
let output = document.querySelector('.output');
let loading = document.querySelector('.loading');

form.onsubmit = async (ev) => {
    ev.preventDefault();
    output.textContent = 'Summarizing, please wait...';
    loading.style.display = 'block';
    let fileInput = document.getElementById('pdfInput');
    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append('file', file);
    try {
        let stream = streamGemini({
            model: 'gemini-pro',
            streamURL: "/api/doc",
            formData: formData
        });
        let buffer = [];
        let md = new markdownit();
        for await (let chunk of stream) {
            loading.style.display = 'none';
            buffer.push(chunk);
            output.innerHTML = md.render(buffer.join(''));
        }
    } catch (e) {
        output.innerHTML += '<hr>' + e;
    }
};