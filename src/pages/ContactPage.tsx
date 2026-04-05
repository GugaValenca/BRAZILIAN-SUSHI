import { useState } from "react";
import { motion } from "framer-motion";
import { Phone, Mail, MessageCircle, Clock, MapPin, Send } from "lucide-react";
import SectionHeading from "@/components/SectionHeading";

const contactInfo = [
  { icon: Phone, label: "Phone", value: "(555) 123-4567", href: "tel:+15551234567" },
  { icon: Mail, label: "Email", value: "hello@braziliansushi.com", href: "mailto:hello@braziliansushi.com" },
  { icon: MessageCircle, label: "WhatsApp", value: "Chat with us", href: "https://wa.me/15551234567" },
  { icon: MessageCircle, label: "Telegram", value: "@braziliansushi", href: "https://t.me/braziliansushi" },
];

const ContactPage = () => {
  const [sent, setSent] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSent(true);
  };

  return (
    <div className="min-h-screen pt-24 md:pt-28 pb-16">
      <div className="container">
        <SectionHeading
          label="Reach Out"
          title="Contact Us"
          subtitle="Questions, catering inquiries, or feedback — we'd love to hear from you."
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-5xl mx-auto">
          {/* Info */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {contactInfo.map((c) => (
                <a
                  key={c.label}
                  href={c.href}
                  target={c.href.startsWith("http") ? "_blank" : undefined}
                  rel="noopener noreferrer"
                  className="bg-card border border-border rounded-xl p-5 hover:border-primary/30 transition-colors group"
                >
                  <c.icon className="w-5 h-5 text-primary mb-2 group-hover:scale-110 transition-transform" />
                  <p className="text-xs text-muted-foreground">{c.label}</p>
                  <p className="font-semibold text-sm mt-0.5">{c.value}</p>
                </a>
              ))}
            </div>

            <div className="bg-card border border-border rounded-xl p-6 space-y-4">
              <div className="flex items-start gap-3">
                <Clock className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <h4 className="font-semibold text-sm">Business Hours</h4>
                  <p className="text-muted-foreground text-sm mt-1">
                    Mon – Sat: 11:00 AM – 10:00 PM<br />
                    Sunday: 12:00 PM – 9:00 PM
                  </p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <MapPin className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <h4 className="font-semibold text-sm">Delivery Area</h4>
                  <p className="text-muted-foreground text-sm mt-1">
                    We deliver within 8 miles of downtown. Free delivery on orders over $35.
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-card border border-border rounded-xl p-6">
              <h4 className="font-semibold text-sm mb-2">Pickup Instructions</h4>
              <p className="text-muted-foreground text-sm leading-relaxed">
                Pickup orders are available at our kitchen entrance on Main Street. 
                Please have your order confirmation ready. Curbside pickup is available — 
                call us when you arrive and we'll bring it out.
              </p>
            </div>
          </motion.div>

          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            {sent ? (
              <div className="bg-card border border-primary/20 rounded-xl p-10 text-center">
                <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                  <Send className="w-7 h-7 text-primary" />
                </div>
                <h3 className="text-xl font-display font-bold mb-2">Message Sent!</h3>
                <p className="text-muted-foreground text-sm">
                  Thank you for reaching out. We'll get back to you within 24 hours.
                </p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="bg-card border border-border rounded-xl p-6 md:p-8 space-y-5">
                <div>
                  <label className="text-sm font-medium text-foreground block mb-1.5">Name</label>
                  <input
                    required
                    type="text"
                    placeholder="Your name"
                    className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground block mb-1.5">Email</label>
                  <input
                    required
                    type="email"
                    placeholder="you@email.com"
                    className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground block mb-1.5">Phone (optional)</label>
                  <input
                    type="tel"
                    placeholder="(555) 000-0000"
                    className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium text-foreground block mb-1.5">Message</label>
                  <textarea
                    required
                    rows={4}
                    placeholder="How can we help?"
                    className="w-full bg-background border border-border rounded-lg px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors resize-none"
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-gradient-gold text-primary-foreground py-3.5 rounded-lg font-semibold hover:opacity-90 transition-opacity"
                >
                  Send Message
                </button>
              </form>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
