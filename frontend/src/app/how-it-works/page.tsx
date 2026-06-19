"use client";

import { motion } from "framer-motion";

const workflow = [
  { step: "GitHub Repository", desc: "You provide a public or private GitHub repository URL." },
  { step: "Repository Cloning", desc: "The platform securely clones the repository into an isolated sandbox." },
  { step: "File Parsing", desc: "Code files are extracted, ignoring binaries and node_modules to ensure high signal-to-noise ratio." },
  { step: "Document Chunking", desc: "Files are split into logical overlapping chunks (e.g., functions, classes) for precise retrieval." },
  { step: "Embedding Generation", desc: "Each chunk is passed through an embedding model to capture its deep semantic meaning." },
  { step: "Vector Indexing", desc: "Embeddings are stored in ChromaDB, enabling ultra-fast similarity search." },
  { step: "Semantic Retrieval", desc: "When you ask a question, the system retrieves the most relevant chunks of code." },
  { step: "LLM Reasoning", desc: "The retrieved context is passed to a powerful LLM to synthesize an accurate answer." },
  { step: "AI Response", desc: "You receive an explanation backed by exact file references and code snippets." }
];

export default function HowItWorksPage() {
  return (
    <div className="bg-[#09090B] min-h-screen py-24 px-4">
      <div className="container mx-auto max-w-4xl">
        <div className="mb-16">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-6 text-slate-50">
            How It Works
          </h1>
          <p className="text-xl text-slate-400">
            A transparent look at the Retrieval-Augmented Generation (RAG) pipeline powering RepoLens AI.
          </p>
        </div>

        <div className="space-y-4">
          {workflow.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              className="flex items-start gap-6 p-6 rounded-2xl border border-slate-800 bg-[#111827]"
            >
              <div className="w-12 h-12 shrink-0 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 font-mono font-bold">
                {index + 1}
              </div>
              <div className="pt-2">
                <h3 className="text-lg font-semibold text-slate-50 mb-2">{item.step}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{item.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
