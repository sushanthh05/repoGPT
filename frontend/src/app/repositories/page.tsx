"use client";

import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";

export default function RepositoriesPage() {
  const mockRepos = [
    {
      name: "auth-service-core",
      tech: ["Node.js", "TypeScript", "Express"],
      files: 124,
      chunks: 842,
      status: "Indexed",
      date: "2 hours ago"
    },
    {
      name: "frontend-dashboard",
      tech: ["Next.js", "React", "Tailwind"],
      files: 342,
      chunks: 1512,
      status: "Indexed",
      date: "1 day ago"
    }
  ];

  return (
    <div className="bg-[#09090B] min-h-screen py-16 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
          <div>
            <h1 className="text-3xl font-bold text-slate-50 mb-2">Analyzed Repositories</h1>
            <p className="text-slate-400">View and chat with your previously indexed codebases.</p>
          </div>
          <Button className="bg-gradient-to-r from-violet-600 to-blue-600 text-white border-0 hover:from-violet-500 hover:to-blue-500">
            Analyze New Repository
          </Button>
        </div>

        <div className="relative mb-8 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search repositories..." 
            className="w-full bg-[#111827] border border-slate-800 rounded-lg pl-10 pr-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-violet-500 transition-colors"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockRepos.map((repo) => (
            <div key={repo.name} className="p-6 rounded-2xl border border-slate-800 bg-[#111827] hover:border-slate-700 transition-colors cursor-pointer group">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-semibold text-lg text-slate-50 group-hover:text-blue-400 transition-colors">{repo.name}</h3>
                <span className="px-2.5 py-1 rounded bg-green-500/10 text-green-400 text-xs font-medium border border-green-500/20">
                  {repo.status}
                </span>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-6">
                {repo.tech.map(t => (
                  <span key={t} className="px-2 py-1 bg-slate-800 rounded text-xs text-slate-300">
                    {t}
                  </span>
                ))}
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-slate-800/50">
                <div className="flex items-center gap-4 text-xs text-slate-500">
                  <span>{repo.files} Files</span>
                  <span>{repo.chunks} Chunks</span>
                </div>
                <span className="text-xs text-slate-500">{repo.date}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
