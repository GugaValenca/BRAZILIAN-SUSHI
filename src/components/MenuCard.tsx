import { motion } from "framer-motion";
import { Flame, Leaf } from "lucide-react";

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
  spicy?: boolean;
  vegetarian?: boolean;
  allergens?: string[];
  featured?: boolean;
}

interface MenuCardProps {
  item: MenuItem;
  index?: number;
  onAddToCart?: (item: MenuItem) => void;
}

const MenuCard = ({ item, index = 0, onAddToCart }: MenuCardProps) => (
  <motion.div
    initial={{ opacity: 0, y: 24 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-40px" }}
    transition={{ duration: 0.5, delay: index * 0.08 }}
    className="group bg-card rounded-xl overflow-hidden border border-border hover:border-primary/30 transition-all duration-300"
  >
    <div className="relative aspect-square overflow-hidden bg-secondary/40">
      <img src={item.image} alt={item.name} loading="lazy" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
      {item.featured && (
        <span className="absolute top-3 left-3 bg-gradient-gold text-primary-foreground text-xs font-bold px-3 py-1 rounded-full">
          Featured
        </span>
      )}
      <div className="absolute top-3 right-3 flex gap-1.5">
        {item.spicy && (
          <span className="bg-sushi-red/90 p-1.5 rounded-full" title="Spicy">
            <Flame className="w-3.5 h-3.5 text-foreground" />
          </span>
        )}
        {item.vegetarian && (
          <span className="bg-sushi-green/90 p-1.5 rounded-full" title="Vegetarian">
            <Leaf className="w-3.5 h-3.5 text-foreground" />
          </span>
        )}
      </div>
    </div>
    <div className="p-4">
      <h3 className="font-display font-semibold text-lg">{item.name}</h3>
      <p className="text-muted-foreground text-sm mt-1 line-clamp-2">{item.description}</p>
      {item.allergens && item.allergens.length > 0 && (
        <div className="flex gap-1 mt-2 flex-wrap">
          {item.allergens.map((a) => (
            <span key={a} className="text-[10px] uppercase tracking-wider text-muted-foreground bg-secondary px-2 py-0.5 rounded">
              {a}
            </span>
          ))}
        </div>
      )}
      <div className="flex items-center justify-between mt-4 gap-3">
        <span className="text-primary font-bold text-lg">${item.price.toFixed(2)}</span>
        <button
          type="button"
          onClick={() => onAddToCart?.(item)}
          className="bg-gradient-gold text-primary-foreground text-sm font-semibold px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
        >
          Add to Cart
        </button>
      </div>
    </div>
  </motion.div>
);

export default MenuCard;
