import React from 'react';

function MenuPage() {
  const menuItems = {
    Starters: [
      { name: "Bruschetta", description: "Fresh tomatoes, basil, olive oil, and toasted baguette slices", price: 8.50 },
      { name: "Caesar Salad", description: "Crisp romaine with homemade Caesar dressing", price: 9.00 },
    ],
    "Main Courses": [
      { name: "Grilled Salmon", description: "Served with lemon butter sauce and seasonal vegetables", price: 22.00 },
      { name: "Ribeye Steak", description: "12 oz prime cut with garlic mashed potatoes", price: 28.00 },
      { name: "Vegetable Risotto", description: "Creamy Arborio rice with wild mushrooms", price: 18.00 },
    ],
    Desserts: [
      { name: "Tiramisu", description: "Classic Italian dessert with mascarpone", price: 7.50 },
      { name: "Cheesecake", description: "Creamy cheesecake with berry compote", price: 7.00 },
    ],
    Beverages: [
      { name: "Red Wine (Glass)", description: "A selection of Italian reds", price: 10.00 },
      { name: "White Wine (Glass)", description: "Crisp and refreshing", price: 9.00 },
      { name: "Craft Beer", description: "Local artisan brews", price: 6.00 },
      { name: "Espresso", description: "Strong and aromatic", price: 3.00 },
    ],
  };

  return (
    <div className="menu-page">
      <div className="page-header">
        <h1 className="page-title">Our Menu</h1>
        <p className="page-subtitle">Crafted with passion, served with excellence</p>
      </div>

      {Object.entries(menuItems).map(([category, items]) => (
        <div key={category} className="menu-category">
          <div className="category-header">
            <h3>{category}</h3>
          </div>
          <div className="menu-items">
            {items.map((item, index) => (
              <div key={index} className="menu-item">
                <div className="item-info">
                  <h4>{item.name}</h4>
                  <p className="item-description">{item.description}</p>
                </div>
                <div className="item-price">${item.price.toFixed(2)}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default MenuPage;