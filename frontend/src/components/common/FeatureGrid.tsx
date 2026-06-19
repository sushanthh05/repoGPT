"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Search, BrainCircuit, MessageSquare, ShieldCheck } from "lucide-react";
import { motion } from "framer-motion";

const features = [
  {
    icon: <Search className="w-6 h-6 text-blue-400" />,
    title: "Semantic Search",
    description: "Search code using meaning instead of keywords. Find exactly what you need even without exact matches."
  },
  {
    icon: <BrainCircuit className="w-6 h-6 text-violet-400" />,
    title: "Repository Intelligence",
    description: "Automatically understand architecture, project structure, and tech stacks upon upload."
  },
  {
    icon: <MessageSquare className="w-6 h-6 text-green-400" />,
    title: "AI Assistant",
    description: "Ask complex questions about implementation details and get comprehensive contextual answers."
  },
  {
    icon: <ShieldCheck className="w-6 h-6 text-rose-400" />,
    title: "Source Attribution",
    description: "Every answer includes direct source file references and exact code snippet evidence."
  }
];

export default function FeatureGrid() {
  return (
    <section className="py-24 px-4 bg-[#09090B]">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4 text-slate-50">Enterprise-Grade Intelligence</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">Everything you need to deeply understand and navigate complex codebases.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="p-8 rounded-2xl border border-slate-800 bg-gradient-to-br from-[#111827] to-[#0f1420] hover:border-slate-600 transition-colors"
            >
              <div className="w-12 h-12 rounded-lg bg-slate-800/50 flex items-center justify-center mb-6">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-slate-50 mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
