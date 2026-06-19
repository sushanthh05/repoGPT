"use client";

import { motion } from "framer-motion";

const steps = [
  {
    number: "01",
    title: "Upload Repository",
    description: "Paste any GitHub repository URL."
  },
  {
    number: "02",
    title: "AI Analysis",
    description: "Repository is parsed, chunked, embedded, and indexed."
  },
  {
    number: "03",
    title: "Ask Questions",
    description: "Chat with your repository using natural language."
  }
];

export default function HowItWorks() {
  return (
    <section className="py-24 px-4 container mx-auto">
      <div className="text-center mb-16">
        <h2 className="text-3xl font-bold tracking-tight mb-4 text-slate-50">How It Works</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">Three simple steps to unlock full codebase understanding.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        {steps.map((step, index) => (
          <motion.div
            key={step.number}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ y: -5 }}
            className="p-8 rounded-2xl border border-slate-800 bg-[#111827] shadow-xl hover:border-slate-700 transition-colors"
          >
            <div className="text-violet-500 font-mono text-xl font-bold mb-4">{step.number}</div>
            <h3 className="text-xl font-semibold text-slate-50 mb-3">{step.title}</h3>
            <p className="text-slate-400">{step.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
