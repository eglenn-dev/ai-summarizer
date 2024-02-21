import { streamGemini } from './gemini-api.js';

let form = document.querySelector('form');
let promptInput = document.querySelector('input[name="prompt"]');
let output = document.querySelector('.output');

form.onsubmit = async (ev) => {
  ev.preventDefault();
  // const frame = document.createElement('iframe');
  // frame.src = promptInput.value;
  // const previewSection = document.querySelector('.preview');
  // previewSection.appendChild(frame);
  output.textContent = 'Generating...';

  try {
    // Call the gemini-pro-vision model, and get a stream of results
    let stream = streamGemini({
      model: 'gemini-pro',
      url: promptInput.value,
    });
    // Read from the stream and interpret the output as markdown
    let buffer = [];
    let md = new markdownit();
    for await (let chunk of stream) {
      buffer.push(chunk);
      output.innerHTML = md.render(buffer.join(''));
    }
  } catch (e) {
    output.innerHTML += '<hr>' + e;
  }
};
