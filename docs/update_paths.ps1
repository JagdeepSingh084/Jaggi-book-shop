# PowerShell script to update paths in all book HTML files
$files = Get-ChildItem -Path "d:\ecommerce_trae\books_scraper\docs" -Filter "book_*.html"

foreach ($file in $files) {
    # Read the file content
    $content = Get-Content $file.FullName -Raw
    
    # Update CSS path
    $content = $content -replace '"/static/css/styles.css"', '"static/css/styles.css"'
    
    # Update Font Awesome path
    $content = $content -replace '"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"', '"static/css/all.min.css"'
    
    # Update cart count id to class
    $content = $content -replace '<span id="cart-count">', '<span class="cart-count">'
    
    # Write updated content back to file
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}

Write-Host "All files have been updated."
