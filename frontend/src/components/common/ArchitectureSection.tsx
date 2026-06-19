"use client";

import { motion } from "framer-motion";

const nodes = [
  "Repository",
  "Parser",
  "Chunking",
  "Embeddings",
  "Vector Search",
  "LLM",
  "Answer"
];

export default function ArchitectureSection() {
  return (
    <section className="py-24 px-4 border-y border-slate-800/50 bg-[#09090B]/50">
      <div className="container mx-auto max-w-5xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4 text-slate-50">How It Works Under The Hood</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">A seamless pipeline transforming raw code into semantic intelligence.</p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-2 md:gap-4 flex-wrap">
          {nodes.map((node, index) => (
            <div key={node} className="flex items-center gap-2 md:gap-4">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="px-6 py-3 rounded-lg border border-slate-700 bg-slate-800/50 text-slate-300 font-medium text-sm text-center shadow-lg whitespace-nowrap"
              >
                {node}
              </motion.div>
              {index < nodes.length - 1 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  whileInView={{ opacity: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.4, delay: (index * 0.1) + 0.1 }}
                  className="text-slate-600 rotate-90 md:rotate-0"
                >
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
