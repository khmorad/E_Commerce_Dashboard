import pandas as pd

data = {
    'id': list(range(1, 11)),
    'seller_name': [
        'BOOK INDUSTRIES', 'Walmart.com', 'JIYA EXPORTS', 'Book Outlet USA', 'SHOPPINGSS',
        'JIYA EXPORTS', 'Walmart.com', 'Walmart.com', 'BOOK INDUSTRIES', 'JIYA EXPORTS'
    ],
    'item_price': [
        19, 7, 9, 6, 10, 10, 10, 8, 10, 10
    ],
    'Item_line_price': [
        '$19.99', '$7.49', '$9.10', '$6.99', '$10.50', '$10.15', '$10.20', '$8.97', '$10.99', '$10.55'
    ],
    'availability': [
        True, True, True, True, True, True, True, True, True, True
    ],
    'avg_rating': [
        5, 4, 4, 4, 4, 4, 4, 4, 4, 4
    ],
    'reviews': [
        16, 50, 115, 94, 30, 14, 28, 5, 11, 186
    ],
    'item_name': [
        'The Wrinkle in Time Boxed Set, Includes 5 Book...',
        'Girl in Pieces (Paperback)',
        'It Starts with Us : A Novel (Paperback)',
        'Verity (Paperback)',
        'Twisted: Twisted Love (Paperback)',
        'Things We Never Got Over (Knockemout)Paperback...',
        'Never After: Hooked (Paperback)',
        'The Maple Hills: Icebreaker (Paperback)',
        'Shatter Me: Shatter Me Series 6-Book Box Set: ...',
        'Dreamland Billionaires: The Fine Print (Series...'
    ]
}

# Create DataFrame from the provided data
df = pd.DataFrame(data)

# Set 'id' as the index of the DataFrame
df.set_index('id', inplace=True)


