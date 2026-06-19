import Hero from "@/components/common/Hero";
import TechStack from "@/components/common/TechStack";
import HowItWorks from "@/components/common/HowItWorks";
import FeatureGrid from "@/components/common/FeatureGrid";
import ProductPreview from "@/components/common/ProductPreview";
import ArchitectureSection from "@/components/common/ArchitectureSection";
import CTASection from "@/components/common/CTASection";

export default function Home() {
  return (
    <div className="flex flex-col flex-1 bg-[#09090B]">
      <Hero />
      <TechStack />
      <HowItWorks />
      <FeatureGrid />
      <ProductPreview />
      <ArchitectureSection />
      <CTASection />
    </div>
  );
}
