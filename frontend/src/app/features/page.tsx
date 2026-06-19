"use client";

import { motion } from "framer-motion";
import { Search, BrainCircuit, MessageSquare, ShieldCheck, Network, Database } from "lucide-react";

const features = [
  {
    icon: <Search className="w-6 h-6 text-blue-400" />,
    title: "Semantic Repository Search",
    description: "Search code using meaning instead of keywords. Our embedding models understand the intent behind your query, finding relevant snippets even without exact matches."
  },
  {
    icon: <BrainCircuit className="w-6 h-6 text-violet-400" />,
    title: "Repository Intelligence",
    description: "Automatically detect the architecture, tech stack, entry points, and project structure the moment a repository is uploaded."
  },
  {
    icon: <MessageSquare className="w-6 h-6 text-green-400" />,
    title: "AI Repository Assistant",
    description: "Ask complex implementation questions using natural language. The AI acts as a senior engineer who has memorized the entire codebase."
  },
  {
    icon: <ShieldCheck className="w-6 h-6 text-rose-400" />,
    title: "Source Attribution",
    description: "Every answer includes direct references to the supporting files and exact code snippet evidence so you never have to blindly trust the AI."
  },
  {
    icon: <Network className="w-6 h-6 text-amber-400" />,
    title: "Architecture Analysis",
    description: "Understand how components interact across the repository. See the big picture before diving into individual files."
  },
  {
    icon: <Database className="w-6 h-6 text-cyan-400" />,
    title: "Context-Aware Retrieval",
    description: "Powered by advanced embeddings, highly optimized vector search, and state-of-the-art retrieval-augmented generation (RAG)."
  }
];

export default function FeaturesPage() {
  return (
    <div className="bg-[#09090B] min-h-screen py-24 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-6 text-slate-50">
            Platform Features
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl">
            RepoLens AI combines deep static analysis with state-of-the-art LLMs to give you an unprecedented understanding of your code.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="p-8 rounded-2xl border border-slate-800 bg-[#111827] shadow-xl hover:border-slate-600 transition-colors"
            >
              <div className="w-12 h-12 rounded-lg bg-slate-800/80 flex items-center justify-center mb-6">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-slate-50 mb-3">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed text-sm">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
