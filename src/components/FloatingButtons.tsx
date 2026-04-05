import { Phone, MessageCircle } from "lucide-react";

const FloatingButtons = () => (
  <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
    <a
      href="https://wa.me/15551234567"
      target="_blank"
      rel="noopener noreferrer"
      className="w-14 h-14 rounded-full bg-sushi-green flex items-center justify-center shadow-lg hover:scale-110 transition-transform"
      aria-label="WhatsApp"
    >
      <MessageCircle className="w-6 h-6 text-foreground" />
    </a>
    <a
      href="tel:+15551234567"
      className="w-14 h-14 rounded-full bg-gradient-gold flex items-center justify-center shadow-lg hover:scale-110 transition-transform md:hidden"
      aria-label="Call"
    >
      <Phone className="w-6 h-6 text-primary-foreground" />
    </a>
  </div>
);

export default FloatingButtons;
