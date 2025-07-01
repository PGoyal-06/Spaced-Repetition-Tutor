import React, { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import FileUploader from "./components/FileUploader";
import FlashcardReview from "./components/FlashcardReview";
import "./index.css";
import TypewriterText from "./components/TypewriterText";

const queryClient = new QueryClient();

export default function App() {
  const [uploaded, setUploaded] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen relative flex flex-col">
        {/* Header */}
        <header className="absolute top-6 left-6">
          <div className="flex flex-col">
            <h1 className="site-title text-4xl md:text-5xl drop-shadow-lg">
              Spaced-Repetition Tutor
            </h1>
            <div className="byline text-xs md:text-sm mt-1 text-white/80 ml-auto">
              By <TypewriterText text="Parth Goyal" />
            </div>
          </div>
        </header>

        {/* Main glass card */}
        <div className="flex-grow flex items-center justify-center px-4">
          <div className="glass glow p-10 md:p-12 max-w-xl w-full mt-32 space-y-8 shadow-2xl transition-all duration-300 backdrop-blur-md">
            {!uploaded ? (
              <>
                <h2 className="glass-heading text-xl md:text-2xl leading-snug text-white/90 text-center drop-shadow-sm">
                  Upload your lecture PDF and learn with AI-generated flashcards
                </h2>

                <FileUploader onDone={() => setUploaded(true)} />
              </>
            ) : (
              <FlashcardReview />
            )}
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}
