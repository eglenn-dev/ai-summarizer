export async function* streamGemini({
  model = 'gemini-2.0-flash',
  streamURL = '',
  url = '',
  formData = ''
} = {}) {
  // Send the prompt to the Python backend
  // Call API defined in main.py
  if (formData != '') {
    let response = await fetch(streamURL, {
      method: "POST",
      body: formData
    });
    yield* streamResponseChunks(response);
  } else if (url != '') {
    let response = await fetch(streamURL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ model, url })
    });
    yield* streamResponseChunks(response);
  }
}

/**
 * A helper that streams text output chunks from a fetch() response.
 */
async function* streamResponseChunks(response) {
  let buffer = '';

  const CHUNK_SEPARATOR = '\n\n';

  let processBuffer = async function* (streamDone = false) {
    while (true) {
      let flush = false;
      let chunkSeparatorIndex = buffer.indexOf(CHUNK_SEPARATOR);
      if (streamDone && chunkSeparatorIndex < 0) {
        flush = true;
        chunkSeparatorIndex = buffer.length;
      }
      if (chunkSeparatorIndex < 0) {
        break;
      }

      let chunk = buffer.substring(0, chunkSeparatorIndex);
      buffer = buffer.substring(chunkSeparatorIndex + CHUNK_SEPARATOR.length);
      chunk = chunk.replace(/^data:\s*/, '').trim();
      if (!chunk) {
        if (flush) break;
        continue;
      }
      let { error, text, faviconURL } = JSON.parse(chunk);
      if (error) {
        console.error(error);
        throw new Error(error?.message || JSON.stringify(error));
      }
      if (faviconURL) {
        const sourceImage = document.querySelector('#destFaviconImage');
        sourceImage.src = faviconURL;
      }
      yield text;
      if (flush) break;
    }
  };

  const reader = response.body.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read()
      if (done) break;
      buffer += new TextDecoder().decode(value);
      console.log(new TextDecoder().decode(value));
      yield* processBuffer();
    }
  } finally {
    reader.releaseLock();
  }

  yield* processBuffer(true);
}
