document.addEventListener('DOMContentLoaded', () => {
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCookie('csrftoken');

    // Attach to all elements with data-track-ui
    const trackableElements = document.querySelectorAll('[data-track-ui]');
    
    trackableElements.forEach(element => {
        element.addEventListener('click', (event) => {
            const elementId = element.id || element.getAttribute('data-track-id') || 'unknown';
            const eventType = element.getAttribute('data-track-event') || 'click';
            
            // Collect metadata if provided via data-track-meta
            let metadata = {};
            const metaAttr = element.getAttribute('data-track-meta');
            if (metaAttr) {
                try {
                    metadata = JSON.parse(metaAttr);
                } catch (e) {
                    console.warn('Invalid JSON in data-track-meta');
                }
            }

            const data = {
                element_id: elementId,
                event_type: eventType,
                page_url: window.location.href,
                metadata: metadata
            };

            fetch('/track-ui-movement/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            }).catch(error => {
                console.error('Error tracking UI movement:', error);
            });
        });
    });
});
