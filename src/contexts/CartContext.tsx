import { createContext, useContext, useEffect, useState } from "react";

import type { NormalizedMenuItem } from "@/lib/catalog";

interface CartItem {
  item: NormalizedMenuItem;
  quantity: number;
}

interface CartContextValue {
  items: CartItem[];
  totalItems: number;
  subtotal: number;
  addItem: (item: NormalizedMenuItem) => void;
  removeItem: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  clearCart: () => void;
}

const CartContext = createContext<CartContextValue | undefined>(undefined);
const STORAGE_KEY = "brazilian-sushi-cart";

export const CartProvider = ({ children }: { children: React.ReactNode }) => {
  const [items, setItems] = useState<CartItem[]>([]);

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) return;
    try {
      setItems(JSON.parse(stored) as CartItem[]);
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const addItem = (item: NormalizedMenuItem) => {
    setItems((current) => {
      const existing = current.find((entry) => entry.item.id === item.id);
      if (existing) {
        return current.map((entry) =>
          entry.item.id === item.id ? { ...entry, quantity: entry.quantity + 1 } : entry,
        );
      }
      return [...current, { item, quantity: 1 }];
    });
  };

  const removeItem = (itemId: string) => {
    setItems((current) => current.filter((entry) => entry.item.id !== itemId));
  };

  const updateQuantity = (itemId: string, quantity: number) => {
    setItems((current) =>
      current
        .map((entry) => (entry.item.id === itemId ? { ...entry, quantity } : entry))
        .filter((entry) => entry.quantity > 0),
    );
  };

  const clearCart = () => setItems([]);

  const totalItems = items.reduce((sum, entry) => sum + entry.quantity, 0);
  const subtotal = items.reduce((sum, entry) => sum + entry.item.price * entry.quantity, 0);

  return (
    <CartContext.Provider value={{ items, totalItems, subtotal, addItem, removeItem, updateQuantity, clearCart }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
};
