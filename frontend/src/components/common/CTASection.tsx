import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function CTASection() {
  return (
    <section className="py-32 px-4 relative overflow-hidden bg-[#09090B]">
      {/* Accent Gradient Background */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-4xl h-[400px] bg-gradient-to-r from-[#7C3AED]/20 to-[#2563EB]/20 blur-[100px] rounded-full pointer-events-none" />
      
      <div className="container mx-auto text-center relative z-10">
        <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6 text-slate-50">
          Ready To Understand Any Repository?
        </h2>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-10">
          Analyze GitHub repositories using AI-powered semantic understanding.
        </p>
        
        <Link href="/repositories">
          <Button size="lg" className="px-8 h-14 text-lg bg-gradient-to-r from-violet-600 to-blue-600 hover:from-violet-500 hover:to-blue-500 text-white border-0">
            Start Analyzing
          </Button>
        </Link>
      </div>
    </section>
  );
}
