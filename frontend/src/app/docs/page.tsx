export default function DocsPage() {
  return (
    <div className="bg-[#09090B] min-h-screen py-24 px-4">
      <div className="container mx-auto max-w-3xl">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-12 text-slate-50">
          Documentation
        </h1>

        <div className="space-y-16">
          <section>
            <h2 className="text-2xl font-semibold text-slate-50 mb-4 border-b border-slate-800 pb-2">What Is RepoLens AI?</h2>
            <p className="text-slate-400 leading-relaxed mb-4">
              RepoLens AI is an advanced repository intelligence platform designed for developers. It ingests whole GitHub repositories, parses their structure, and exposes them through a highly contextual semantic search and AI chat interface. It acts as an interactive documentation layer for undocumented or complex codebases.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-50 mb-4 border-b border-slate-800 pb-2">Supported Languages</h2>
            <p className="text-slate-400 leading-relaxed mb-4">
              The platform uses intelligent file chunking strategies optimized for the following languages:
            </p>
            <ul className="list-disc list-inside text-slate-400 space-y-2 ml-4">
              <li>TypeScript / JavaScript</li>
              <li>Python</li>
              <li>Go</li>
              <li>Java</li>
              <li>Rust</li>
              <li>C / C++</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-slate-50 mb-4 border-b border-slate-800 pb-2">Frequently Asked Questions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-medium text-slate-200 mb-2">Are my private repositories secure?</h3>
                <p className="text-slate-400 text-sm">Yes. Repositories are cloned into isolated, ephemeral sandboxes for parsing. The code is chunked and stored securely in our vector database, and original source files are deleted immediately after indexing.</p>
              </div>
              <div>
                <h3 className="text-lg font-medium text-slate-200 mb-2">Can I analyze monorepos?</h3>
                <p className="text-slate-400 text-sm">Yes, monorepos are supported. However, extremely large monorepos (over 10,000 files) may take several minutes to index completely.</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
