import { useState, useMemo } from "react";
import { Search, Flame, Leaf, Filter } from "lucide-react";
import { motion } from "framer-motion";
import SectionHeading from "@/components/SectionHeading";
import MenuCard from "@/components/MenuCard";
import { categories, menuItems } from "@/data/menuData";

const MenuPage = () => {
  const [activeCategory, setActiveCategory] = useState("All");
  const [search, setSearch] = useState("");
  const [showSpicy, setShowSpicy] = useState(false);
  const [showVeg, setShowVeg] = useState(false);

  const filtered = useMemo(() => {
    let items = menuItems;
    if (activeCategory !== "All") items = items.filter((i) => i.category === activeCategory);
    if (showSpicy) items = items.filter((i) => i.spicy);
    if (showVeg) items = items.filter((i) => i.vegetarian);
    if (search.trim()) {
      const q = search.toLowerCase();
      items = items.filter(
        (i) => i.name.toLowerCase().includes(q) || i.description.toLowerCase().includes(q)
      );
    }
    return items;
  }, [activeCategory, search, showSpicy, showVeg]);

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container">
        <SectionHeading
          label="Our Selection"
          title="The Menu"
          subtitle="Handcrafted with the finest ingredients. Something for every palate."
        />

        {/* Search & Filters */}
        <div className="max-w-3xl mx-auto mb-10 space-y-4">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search the menu..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-card border border-border rounded-xl pl-12 pr-4 py-3.5 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
            />
          </div>

          <div className="flex items-center gap-3 flex-wrap">
            <Filter className="w-4 h-4 text-muted-foreground" />
            {categories.map((c) => (
              <button
                key={c}
                onClick={() => setActiveCategory(c)}
                className={`text-sm px-4 py-2 rounded-full border transition-all ${
                  activeCategory === c
                    ? "bg-gradient-gold text-primary-foreground border-primary"
                    : "border-border text-muted-foreground hover:border-primary/40 hover:text-foreground"
                }`}
              >
                {c}
              </button>
            ))}
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => setShowSpicy(!showSpicy)}
              className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border transition-all ${
                showSpicy ? "bg-sushi-red/20 border-sushi-red/40 text-accent" : "border-border text-muted-foreground"
              }`}
            >
              <Flame className="w-3.5 h-3.5" /> Spicy
            </button>
            <button
              onClick={() => setShowVeg(!showVeg)}
              className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border transition-all ${
                showVeg ? "bg-sushi-green/20 border-sushi-green/40 text-sushi-green" : "border-border text-muted-foreground"
              }`}
            >
              <Leaf className="w-3.5 h-3.5" /> Vegetarian
            </button>
          </div>
        </div>

        {/* Items grid */}
        {filtered.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filtered.map((item, i) => (
              <MenuCard key={item.id} item={item} index={i} />
            ))}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20"
          >
            <p className="text-muted-foreground text-lg">No items found. Try adjusting your filters.</p>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default MenuPage;
