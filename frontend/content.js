// Wrap the entire script in an immediately invoked function expression (IIFE)
(function() {
    // Function to generate a random spam probability
    function getRandomSpamProbability() {
        return Math.random();
    }

    // Function to create and insert the spam probability element
    function insertSpamProbability(commentElement, probability) {
        if (commentElement.querySelector('.spam-probability')) return;

        const spamProbEl = document.createElement('span');
        spamProbEl.className = 'spam-probability';
        spamProbEl.textContent = `Spam Probability: ${(probability * 100).toFixed(2)}%`;
        spamProbEl.style.cssText = `
            display: inline-block;
            margin-left: 10px;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            color: white;
            background-color: ${probability > 0.5 ? 'red' : 'green'};
        `;
        const headerAuthor = commentElement.querySelector('#header-author');
        if (headerAuthor) {
            headerAuthor.appendChild(spamProbEl);
        }
    }

    // Function to process comments
    function processComments() {
        const comments = document.querySelectorAll('ytd-comment-thread-renderer');
        console.log(`Processing ${comments.length} comments`);
        comments.forEach((comment, index) => {
            const contentText = comment.querySelector('#content-text');
            if (contentText && !comment.querySelector('.spam-probability')) {
                const probability = getRandomSpamProbability();
                insertSpamProbability(comment, probability);
                console.log(`Processed comment ${index + 1}`);
            }
        });
    }

    // Function to check for comments and set up observers
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

    // Function to handle page navigation
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
})();
