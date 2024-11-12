const $document = document;
const $chatbot = $document.querySelector('.chatbot');
const $chatbotMessages = $document.querySelector('.chatbot__messages');
const $chatbotInput = $document.querySelector('.chatbot__input');
const $chatbotSubmit = $document.querySelector('.chatbot__submit');
const $chatbotHeader = $document.querySelector('.chatbot__header');

$chatbotHeader.addEventListener('click', () => {
  toggleChatbot();
}, false);

$chatbotSubmit.addEventListener('click', () => {
  sendMessage();
}, false);

$chatbotInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

const toggleChatbot = () => {
  toggle($chatbot, 'chatbot--closed');
  if (!$chatbot.classList.contains('chatbot--closed')) {
    $chatbotInput.focus();
  }
};

const sendMessage = () => {
  const text = $chatbotInput.value;
  if (text.trim() === '') return;

  addMessage('user', text);

  fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: text })
  })
  .then(response => response.json())
  .then(data => {
    const aiResponse = data.message;
    addMessage('ai', aiResponse);
  })
  .catch(error => {
    console.error('Error:', error);
    addMessage('ai', 'Sorry, something went wrong.');
  });

  $chatbotInput.value = '';
};

const addMessage = (sender, content) => {
  const senderClass = sender === 'user' ? 'is-user' : 'is-ai';

  // Check if the content starts and ends with triple backticks
  if (content.startsWith('```') && content.endsWith('```')) {
    // Render code block with copy button
    $chatbotMessages.innerHTML += `
      <li class='${senderClass} animation'>
        <div class='chatbot__message code-block'>
          <code>${content.slice(3, -3)}</code>
          <button class='copy-code-btn'>Copy Code</button>
        </div>
        <span class='chatbot__arrow ${sender === 'user' ? 'chatbot__arrow--right' : 'chatbot__arrow--left'}'></span>
      </li>`;
  } else {
    // Render normal message
    $chatbotMessages.innerHTML += `
      <li class='${senderClass} animation'>
        <div class='chatbot__message'>${content}</div>
        <span class='chatbot__arrow ${sender === 'user' ? 'chatbot__arrow--right' : 'chatbot__arrow--left'}'></span>
      </li>`;
  }
  
  // Attach event listener to copy code button
  const $copyCodeBtn = document.querySelector('.copy-code-btn');
  if ($copyCodeBtn) {
    $copyCodeBtn.addEventListener('click', () => {
      copyCode(content.slice(3, -3));
    });
  }
};

const copyCode = (codeContent) => {
  const tempTextArea = document.createElement('textarea');
  tempTextArea.value = codeContent;
  document.body.appendChild(tempTextArea);
  tempTextArea.select();
  document.execCommand('copy');
  document.body.removeChild(tempTextArea);
};


const toggle = (element, klass) => {
  const classes = element.className.match(/\S+/g) || [],
  index = classes.indexOf(klass);
  index >= 0 ? classes.splice(index, 1) : classes.push(klass);
  element.className = classes.join(' ');
};
