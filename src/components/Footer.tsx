import { Facebook, Ghost, Instagram, Music2, type LucideIcon } from "lucide-react";
import { Link } from "react-router-dom";

const socials = [
  { label: "Instagram", href: "https://instagram.com/braziliansushi", icon: Instagram },
  { label: "TikTok", href: "https://tiktok.com/@braziliansushi", icon: Music2 },
  { label: "Facebook", href: "https://facebook.com/braziliansushi", icon: Facebook },
  { label: "Snapchat", href: "https://snapchat.com/add/braziliansushi", icon: Ghost },
] satisfies Array<{ label: string; href: string; icon: LucideIcon }>;

const footerLinks = [
  { to: "/", label: "Home" },
  { to: "/menu", label: "Menu" },
  { to: "/contact", label: "Contact" },
  { to: "/track-order", label: "Track Order" },
  { to: "/account", label: "Account" },
];

const Footer = () => (
  <footer className="border-t border-border bg-gradient-card">
    <div className="container py-12 md:py-16">
      <div className="max-w-6xl mx-auto space-y-10">
        <div className="text-center max-w-2xl mx-auto">
          <h3 className="text-2xl md:text-3xl font-display font-bold text-gradient-gold mb-4">Brazilian Sushi</h3>
          <p className="text-muted-foreground text-sm md:text-base leading-relaxed">
            Premium sushi crafted with Japanese precision and Brazilian soul, designed exclusively for delivery and takeout.
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 md:gap-4">
          {footerLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className="inline-flex items-center justify-center rounded-full border border-border bg-secondary/70 px-4 py-2 text-sm text-muted-foreground transition-all hover:border-primary/30 hover:text-foreground hover:bg-secondary"
            >
              {link.label}
            </Link>
          ))}
        </div>

        <div className="flex items-center justify-center gap-4">
          {socials.map((social) => (
            <a
              key={social.label}
              href={social.href}
              target="_blank"
              rel="noopener noreferrer"
              className="w-10 h-10 rounded-full border border-border/60 bg-secondary/90 flex items-center justify-center transition-all hover:bg-primary/20 hover:border-primary/30"
              aria-label={social.label}
            >
              <social.icon className="w-5 h-5" strokeWidth={1.9} />
            </a>
          ))}
        </div>
      </div>

      <div className="divider-gold mt-10 mb-6" />
      <p className="text-center text-xs text-muted-foreground">© {new Date().getFullYear()} Brazilian Sushi. All rights reserved.</p>
    </div>
  </footer>
);

export default Footer;
