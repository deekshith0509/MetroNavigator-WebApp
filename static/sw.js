self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : 'No data',
        icon: 'path/to/icon.png', // Path to a notification icon
    };
    event.waitUntil(
        self.registration.showNotification('Metro Alert', options)
    );
});
