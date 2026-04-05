import { Phone, MessageCircle } from "lucide-react";

import { businessInfo } from "@/lib/site";

const FloatingButtons = () => (
  <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
    <a
      href={businessInfo.whatsappHref}
      target="_blank"
      rel="noopener noreferrer"
      className="w-14 h-14 rounded-full bg-sushi-green/95 backdrop-blur-sm flex items-center justify-center shadow-[0_16px_35px_rgba(17,24,39,0.32)] hover:scale-110 hover:-translate-y-0.5 transition-all"
      aria-label="WhatsApp"
    >
      <MessageCircle className="w-6 h-6 text-foreground" />
    </a>
    <a
      href={businessInfo.phoneHref}
      className="w-14 h-14 rounded-full bg-gradient-gold flex items-center justify-center shadow-[0_16px_35px_rgba(17,24,39,0.32)] hover:scale-110 hover:-translate-y-0.5 transition-all md:hidden"
      aria-label="Call"
    >
      <Phone className="w-6 h-6 text-primary-foreground" />
    </a>
  </div>
);

export default FloatingButtons;
