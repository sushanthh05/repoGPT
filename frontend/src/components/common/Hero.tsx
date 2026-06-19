"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative flex flex-col items-center justify-center pt-24 pb-12 px-4 text-center">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-blue-600/20 blur-[120px] rounded-full pointer-events-none" />

      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-5xl md:text-7xl font-bold tracking-tight mb-6 max-w-4xl"
      >
        Turn Any GitHub Repository Into <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-blue-600">Searchable Knowledge</span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        className="text-lg md:text-xl text-slate-400 max-w-2xl mb-10"
      >
        Upload a GitHub repository and instantly explore its architecture, tech stack, implementation details, and source code through natural language.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="flex flex-col sm:flex-row gap-4 mb-16 relative z-10"
      >
        <Link href="/repositories">
          <Button size="lg" className="px-8 h-12 bg-slate-50 text-slate-900 hover:bg-slate-200">
            Analyze Repository
          </Button>
        </Link>
        <Button size="lg" variant="outline" className="px-8 h-12 border-slate-700 hover:bg-slate-800">
          Explore Demo
        </Button>
      </motion.div>
    </section>
  );
}
