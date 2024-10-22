/**
 * Sends a comment to the spam detection endpoint and returns a classification.
 * @param {string} commentBody - The text content of the comment.
 * @returns {Promise<boolean>} A promise that resolves to true if classified as spam, false otherwise.
 */
async function getSpamClassification(commentBody) {
    const endpoint = 'http://localhost:8000/v1/detect'; 
    // const endpoint = 'https://stormy-lowlands-61087-f9957486f73b.herokuapp.com/v1/detect'; 
    // TODO: change this to the actual endpoint

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content: commentBody,
                uuid: crypto.randomUUID(),
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.is_spam;

    } catch (error) {
        console.error('Error calling spam detection API:', error);
        // In case of an error, we'll assume it's not spam
        return false;
    }
}

/**
 * Creates and inserts a spam info pill element into a comment.
 * @param {HTMLElement} commentElement - The comment element to insert the pill into.
 * @param {boolean} isSpam - Whether the comment is classified as spam.
 */
function insertSpamInfoPill(commentElement, isSpam) {
    if (commentElement.querySelector('.spam-info')) return;

    const spamInfoEl = document.createElement('span');
    spamInfoEl.className = 'spam-info';
    spamInfoEl.textContent = isSpam ? 'Potentially Spam' : 'Not Spam';
    spamInfoEl.style.cssText = `
        display: inline-block;
        margin-left: 10px;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        background-color: ${isSpam ? 'red' : 'gray'};
    `;
    const headerAuthor = commentElement.querySelector('#header-author');
    if (headerAuthor) {
        headerAuthor.appendChild(spamInfoEl);
    }
}

/**
 * Processes all comments on the page, adding spam classification indicators.
 */
async function processComments() {
    const comments = document.querySelectorAll('ytd-comment-thread-renderer');
    console.log(`Processing ${comments.length} comments`);
    for (let index = 0; index < comments.length; index++) {
        const comment = comments[index];
        const contentText = comment.querySelector('#content-text');
        if (contentText && !comment.querySelector('.spam-info')) {
            const commentBody = contentText.textContent;
            const isSpam = await getSpamClassification(commentBody);
            insertSpamInfoPill(comment, isSpam);
            console.log(`Processed comment ${index + 1}`);
        }
    }
}

/**
 * Sets up an observer for the comments section and processes existing comments.
 */
function setupCommentObserver() {
    const commentsSection = document.querySelector('ytd-comments');
    if (commentsSection) {
        console.log("Comments section found, setting up observer...");
        
        // Process existing comments
        processComments();

        // Set up the observer for future updates
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    processComments();
                }
            });
        });
        observer.observe(commentsSection, { childList: true, subtree: true });
    } else {
        console.log("Comments section not found, retrying in 1 second...");
        setTimeout(setupCommentObserver, 1000);
    }
}

/**
 * Handles page navigation by re-initializing the comment observer when the URL changes.
 */
function handlePageNavigation() {
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            console.log('URL changed, re-initializing comment observer...');
            setupCommentObserver();
        }
    }).observe(document, {subtree: true, childList: true});
}

// Start the script
console.log("YouTube Comment Spam Detector script loaded");

// Initial setup
setupCommentObserver();
handlePageNavigation();

// Periodically check for new comments
setInterval(processComments, 5000);
