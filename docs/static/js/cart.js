// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Load cart count
    updateCartCount();
    
    // Add to cart buttons - use event delegation for better performance
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart')) {
            e.preventDefault();
            const upc = e.target.dataset.upc;
            addToCart(upc);
        }
    });
});

function updateCartCount() {
    fetch('/api/cart')
        .then(response => response.json())
        .then(cart => {
            const cartCount = Array.isArray(cart) ? 
                cart.reduce((total, item) => total + item.quantity, 0) : 
                Object.values(cart).reduce((total, item) => total + item.quantity, 0);
            
            document.querySelectorAll('.cart-count').forEach(el => {
                el.textContent = cartCount;
            });
        })
        .catch(error => console.error('Error updating cart count:', error));
}

function addToCart(upc) {
    const button = document.querySelector(`.add-to-cart[data-upc="${upc}"]`);
    if (button) button.disabled = true; // Prevent double clicks

    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            upc: upc,
            quantity: 1
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update cart count
            document.querySelectorAll('.cart-count').forEach(el => {
                el.textContent = data.cart_count;
            });
            // Show success message
            showAddedToCartMessage(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAddedToCartMessage('Failed to add item to cart');
    })
    .finally(() => {
        if (button) button.disabled = false; // Re-enable the button
    });
}

function showAddedToCartMessage(message) {
    // Create message element if it doesn't exist
    let messageEl = document.getElementById('cart-message');
    if (!messageEl) {
        messageEl = document.createElement('div');
        messageEl.id = 'cart-message';
        messageEl.className = 'cart-message';
        document.body.appendChild(messageEl);
    }
    
    // Show message
    messageEl.textContent = message || 'Added to cart!';
    messageEl.classList.add('show');
    
    // Hide message after 3 seconds
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 3000);
}