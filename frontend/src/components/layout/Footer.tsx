import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/50 bg-[#09090B] py-12">
      <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
        <div className="flex flex-col items-center md:items-start gap-2">
          <span className="font-bold text-xl tracking-tight text-slate-50">RepoLens AI</span>
          <span className="text-sm text-slate-500">© 2026 RepoLens AI. All rights reserved.</span>
        </div>
        
        <div className="flex flex-col md:flex-row items-start md:items-center gap-12 mt-8 md:mt-0">
          <div className="flex flex-col gap-4">
            <span className="text-slate-50 font-semibold text-sm">Product</span>
            <Link href="/features" className="text-sm text-slate-400 hover:text-white transition-colors">Features</Link>
            <Link href="/how-it-works" className="text-sm text-slate-400 hover:text-white transition-colors">How It Works</Link>
            <Link href="/repositories" className="text-sm text-slate-400 hover:text-white transition-colors">Repositories</Link>
            <Link href="/docs" className="text-sm text-slate-400 hover:text-white transition-colors">Docs</Link>
          </div>
          
          <div className="flex flex-col gap-4">
            <span className="text-slate-50 font-semibold text-sm">Tech Stack</span>
            <span className="text-sm text-slate-400">Next.js</span>
            <span className="text-sm text-slate-400">FastAPI</span>
            <span className="text-sm text-slate-400">LangChain</span>
          </div>

          <div className="flex flex-col gap-4">
            <span className="text-slate-50 font-semibold text-sm">Database</span>
            <span className="text-sm text-slate-400">PostgreSQL</span>
            <span className="text-sm text-slate-400">ChromaDB</span>
            <span className="text-sm text-slate-400">Groq</span>
          </div>

          <div className="flex flex-col gap-4">
            <span className="text-slate-50 font-semibold text-sm">Code</span>
            <Link href="https://github.com" className="text-sm text-slate-400 hover:text-white transition-colors">GitHub Repository</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
