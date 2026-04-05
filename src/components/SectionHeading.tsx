import { motion } from "framer-motion";

interface SectionHeadingProps {
  label?: string;
  title: string;
  subtitle?: string;
}

const SectionHeading = ({ label, title, subtitle }: SectionHeadingProps) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-80px" }}
    transition={{ duration: 0.6 }}
    className="text-center mb-10 md:mb-14"
  >
    {label && (
      <span className="inline-flex items-center gap-3 text-xs uppercase tracking-[0.32em] text-primary/90 font-medium">
        <span className="h-px w-8 bg-primary/35" />
        {label}
        <span className="h-px w-8 bg-primary/35" />
      </span>
    )}
    <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mt-3 mb-4 leading-tight">
      {title}
    </h2>
    {subtitle && (
      <p className="text-muted-foreground max-w-2xl mx-auto leading-relaxed text-sm md:text-base">{subtitle}</p>
    )}
    <div className="divider-gold mt-6 max-w-[120px] mx-auto" />
  </motion.div>
);

export default SectionHeading;
