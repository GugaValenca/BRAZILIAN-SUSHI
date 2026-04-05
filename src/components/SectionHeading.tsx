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
      <span className="text-sm uppercase tracking-[0.2em] text-primary font-medium">
        {label}
      </span>
    )}
    <h2 className="text-3xl md:text-4xl lg:text-5xl font-display font-bold mt-2 mb-4">
      {title}
    </h2>
    {subtitle && (
      <p className="text-muted-foreground max-w-lg mx-auto">{subtitle}</p>
    )}
    <div className="divider-gold mt-6 max-w-[120px] mx-auto" />
  </motion.div>
);

export default SectionHeading;
