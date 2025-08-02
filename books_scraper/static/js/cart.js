// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Load cart count
    updateCartCount();
    
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    if (addToCartButtons) {
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const upc = this.dataset.upc;
                addToCart(upc);
            });
        });
    }
});

function updateCartCount() {
    fetch('/api/cart')
        .then(response => response.json())
        .then(cart => {
            const cartCount = cart.reduce((total, item) => total + item.quantity, 0);
            document.getElementById('cart-count').textContent = cartCount;
        })
        .catch(error => console.error('Error updating cart count:', error));
}

function addToCart(upc) {
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            upc: upc  // Ensure this matches server expectation
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
            // Force DOM update for cart counter
            document.querySelectorAll('.cart-count').forEach(el => {
                el.textContent = data.cart_count;
            });
            showTempMessage(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showTempMessage('Failed to add item to cart');
    });
}

function showAddedToCartMessage() {
    // Create message element if it doesn't exist
    let messageEl = document.getElementById('cart-message');
    if (!messageEl) {
        messageEl = document.createElement('div');
        messageEl.id = 'cart-message';
        messageEl.className = 'cart-message';
        document.body.appendChild(messageEl);
    }
    
    // Show message
    messageEl.textContent = 'Added to cart!';
    messageEl.classList.add('show');
    
    // Hide message after 3 seconds
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 3000);
}