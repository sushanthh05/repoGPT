"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-800/50 bg-[#09090B]/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center px-4 justify-between">
        <Link href="/" className="font-bold text-xl tracking-tight text-slate-50 flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-blue-600 flex items-center justify-center text-white text-sm">
            RL
          </div>
          RepoLens AI
        </Link>
        
        <div className="hidden md:flex gap-8 items-center">
          <Link href="/features" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Features
          </Link>
          <Link href="/how-it-works" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            How It Works
          </Link>
          <Link href="/repositories" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Repositories
          </Link>
          <Link href="/docs" className="text-sm font-medium text-slate-300 hover:text-white transition-colors">
            Docs
          </Link>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/repositories">
            <Button size="sm" className="bg-slate-50 text-slate-900 hover:bg-slate-200 font-medium">
              Analyze Repository
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
