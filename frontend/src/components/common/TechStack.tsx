"use client";

import { motion } from "framer-motion";

const technologies = [
  "Next.js", "TypeScript", "FastAPI", "LangChain", 
  "PostgreSQL", "ChromaDB", "Groq", "GitPython", "Sentence Transformers"
];

export default function TechStack() {
  return (
    <section className="py-10 border-y border-slate-800/50 bg-[#09090B]/50 backdrop-blur-sm overflow-hidden">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm font-medium text-slate-500 mb-6 uppercase tracking-wider">
          Trusted Technologies
        </p>
        <div className="flex flex-wrap justify-center gap-3 md:gap-4 max-w-4xl mx-auto">
          {technologies.map((tech, index) => (
            <motion.div
              key={tech}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="px-4 py-2 rounded-full border border-slate-700 bg-slate-800/30 text-slate-300 text-sm font-medium"
            >
              {tech}
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
