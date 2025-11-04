// /assets/js/page-enhancements.js
document.addEventListener('DOMContentLoaded', () => {
  const faqHeading = document.querySelector('#faq');
  const container = faqHeading ? faqHeading.nextElementSibling : null;
  if (faqHeading && container) {
    let node = container.firstElementChild;
    while (node) {
      if (node.tagName === 'H3') {
        const question = node.textContent.trim();
        const answerParts = [];
        let cursor = node.nextElementSibling;
        while (cursor && cursor.tagName !== 'H3') {
          answerParts.append ? answerParts.append(cursor.outerHTML) : answerParts.push(cursor.outerHTML);
          const toRemove = cursor;
          cursor = cursor.nextElementSibling;
          container.removeChild(toRemove);
        }
        const details = document.createElement('details');
        details.className = 'bg-white rounded-lg border p-4 mb-2';
        const summary = document.createElement('summary');
        summary.className = 'cursor-pointer font-semibold select-none';
        summary.textContent = question;
        const answerWrap = document.createElement('div');
        answerWrap.className = 'pt-2 text-gray-700';
        answerWrap.innerHTML = answerParts.join('');
        details.appendChild(summary);
        details.appendChild(answerWrap);
        container.removeChild(node);
        container.insertBefore(details, cursor || null);
        node = cursor;
      } else {
        node = node.nextElementSibling;
      }
    }
  }
});
