import { Facebook, Ghost, Instagram, Music2, type LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

const socials = [
  { label: "Instagram", href: "https://instagram.com/braziliansushi", icon: Instagram },
  { label: "TikTok", href: "https://tiktok.com/@braziliansushi", icon: Music2 },
  { label: "Facebook", href: "https://facebook.com/braziliansushi", icon: Facebook },
  { label: "Snapchat", href: "https://snapchat.com/add/braziliansushi", icon: Ghost },
] satisfies Array<{ label: string; href: string; icon: LucideIcon }>;

const Footer = () => (
  <footer className="border-t border-border bg-card">
    <div className="container py-12 md:py-16">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
        <div>
          <h3 className="text-2xl font-display font-bold text-gradient-gold mb-4">
            Brazilian Sushi
          </h3>
          <p className="text-muted-foreground text-sm leading-relaxed max-w-xs">
            Premium sushi crafted with Japanese precision and Brazilian soul. 
            Delivery & takeout only.
          </p>
        </div>

        <div>
          <h4 className="font-semibold text-foreground mb-4">Quick Links</h4>
          <div className="flex flex-col gap-2">
            <Link to="/" className="text-sm text-muted-foreground hover:text-primary transition-colors">Home</Link>
            <Link to="/menu" className="text-sm text-muted-foreground hover:text-primary transition-colors">Menu</Link>
            <Link to="/contact" className="text-sm text-muted-foreground hover:text-primary transition-colors">Contact</Link>
          </div>
        </div>

        <div>
          <h4 className="font-semibold text-foreground mb-4">Follow Us</h4>
          <div className="flex gap-4">
            {socials.map((s) => (
              <a
                key={s.label}
                href={s.href}
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center hover:bg-primary/20 transition-colors"
                aria-label={s.label}
              >
                <s.icon className="w-5 h-5" strokeWidth={1.9} />
              </a>
            ))}
          </div>
        </div>
      </div>

      <div className="divider-gold mt-10 mb-6" />
      <p className="text-center text-xs text-muted-foreground">
        © {new Date().getFullYear()} Brazilian Sushi. All rights reserved.
      </p>
    </div>
  </footer>
);

export default Footer;
