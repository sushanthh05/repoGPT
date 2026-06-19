"use client";

import { motion } from "framer-motion";

export default function ProductPreview() {
  return (
    <section className="py-24 px-4 bg-[#09090B] relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-violet-600/10 blur-[120px] rounded-full pointer-events-none" />

      <div className="container mx-auto max-w-6xl relative z-10">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4 text-slate-50">See It In Action</h2>
          <p className="text-slate-400 max-w-2xl mx-auto">Experience a fully contextual, semantic understanding of your code.</p>
        </div>

        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left Card: Repository Overview */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="flex-[1.2] rounded-2xl border border-slate-800 bg-[#111827]/90 backdrop-blur-xl p-8 shadow-2xl"
          >
            <div className="mb-8">
              <h3 className="text-xl font-bold text-slate-50">Repository Overview</h3>
              <p className="text-sm text-slate-400">auth-service-core</p>
            </div>

            <div className="space-y-8">
              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Tech Stack</h4>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1.5 rounded-md bg-[#09090B] text-slate-300 text-xs font-medium border border-slate-800">Node.js</span>
                  <span className="px-3 py-1.5 rounded-md bg-[#09090B] text-slate-300 text-xs font-medium border border-slate-800">Express</span>
                  <span className="px-3 py-1.5 rounded-md bg-[#09090B] text-slate-300 text-xs font-medium border border-slate-800">Redis</span>
                </div>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Languages</h4>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1.5 rounded-md bg-blue-500/10 text-blue-400 text-xs font-medium border border-blue-500/20">TypeScript (85%)</span>
                  <span className="px-3 py-1.5 rounded-md bg-yellow-500/10 text-yellow-400 text-xs font-medium border border-yellow-500/20">JavaScript (15%)</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-[#09090B] border border-slate-800">
                  <div className="text-3xl font-bold text-slate-50 mb-1">124</div>
                  <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Files</div>
                </div>
                <div className="p-4 rounded-xl bg-[#09090B] border border-slate-800">
                  <div className="text-3xl font-bold text-slate-50 mb-1">842</div>
                  <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Chunks</div>
                </div>
              </div>

              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Architecture</h4>
                <p className="text-sm text-slate-300 leading-relaxed">
                  Microservice handling global authentication and session management. Leverages JWTs for stateless auth and Redis for instant token blacklisting.
                </p>
              </div>
            </div>
          </motion.div>

          {/* Right Card: AI Chat */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex-[1.8] rounded-2xl border border-slate-800 bg-[#111827]/90 backdrop-blur-xl flex flex-col shadow-2xl overflow-hidden"
          >
            <div className="px-6 py-4 border-b border-slate-800 bg-[#09090B]/50 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-50">AI Chat</h3>
              <span className="flex items-center gap-2 text-xs font-medium text-green-400 bg-green-400/10 px-2 py-1 rounded border border-green-400/20">
                <div className="w-1.5 h-1.5 rounded-full bg-green-400" />
                Connected
              </span>
            </div>
            
            <div className="p-8 flex-1 flex flex-col justify-center space-y-8">
              {/* User Message */}
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-slate-800 shrink-0 flex items-center justify-center text-sm font-bold text-slate-300 border border-slate-700 shadow-sm">U</div>
                <div className="mt-2 bg-[#09090B] px-5 py-3 rounded-2xl rounded-tl-sm border border-slate-800">
                  <p className="text-slate-200">How authentication works?</p>
                </div>
              </div>

              {/* AI Message */}
              <div className="flex gap-4">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-violet-600 to-blue-600 shrink-0 flex items-center justify-center text-sm font-bold text-white shadow-md shadow-violet-500/20">RL</div>
                <div className="mt-2 w-full">
                  <p className="text-slate-300 leading-relaxed mb-6 bg-[#09090B] px-5 py-4 rounded-2xl rounded-tl-sm border border-slate-800">
                    JWT authentication is implemented using middleware and token validation services.
                  </p>
                  
                  <div>
                    <h5 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Sources</h5>
                    <div className="flex gap-3">
                      <div className="px-4 py-2 rounded-lg bg-[#09090B] border border-slate-800 flex items-center gap-2 hover:border-slate-600 transition-colors cursor-pointer">
                        <svg className="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                        <span className="text-sm font-medium text-slate-300">jwt.ts</span>
                      </div>
                      <div className="px-4 py-2 rounded-lg bg-[#09090B] border border-slate-800 flex items-center gap-2 hover:border-slate-600 transition-colors cursor-pointer">
                        <svg className="w-4 h-4 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                        <span className="text-sm font-medium text-slate-300">auth_controller.ts</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
