import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "../services/api";

export default function FlashcardReview() {
  const queryClient = useQueryClient();
  const [showAnswer, setShowAnswer] = useState(false);

  // 1) fetch next due card
  const { data: card, isLoading } = useQuery({
    queryKey: ["nextReview", { userId: 1 }],
    queryFn: () => api.get(`/reviews/next?user_id=1`).then((res) => res.data),
    retry: false,
  });

  // 2) submit rating, then refetch
  const reviewMutation = useMutation({
    mutationFn: ({ flashcardId, quality }) =>
      api.post(`/reviews/${flashcardId}`, {
        user_id: 1,
        quality,
      }),
    onSuccess: () => {
      setShowAnswer(false);
      queryClient.invalidateQueries(["nextReview", { userId: 1 }]);
    },
  });

  if (isLoading) return null;

  // no cards due
  if (!card || !card.id) {
    return (
      <div className="glass float-note p-8 md:p-10 w-full max-w-lg mx-auto text-center shadow-2xl">
        <p className="text-white/90 text-xl md:text-2xl font-semibold leading-snug drop-shadow-sm">
          <span className="emoji-pulse inline-block">🎉</span> All caught up for
          now —
          <br className="hidden md:inline" />
          come back later!
        </p>
      </div>
    );
  }
  return (
    <div className="glass p-8 md:p-10 space-y-6 w-full max-w-2xl mx-auto text-white shadow-2xl backdrop-blur-lg">
      {/* Question / Answer Box */}
      <div className="text-xl md:text-2xl font-medium leading-snug text-center text-white/90 drop-shadow-sm min-h-[80px] transition-all duration-200">
        {showAnswer ? card.answer : card.question}
      </div>

      {/* Rating Buttons */}
      <div className="flex justify-center gap-2 flex-wrap">
        {[0, 1, 2, 3, 4, 5].map((q) => (
          <button
            key={q}
            className="rating-glow text-lg w-10 h-10 rounded-full font-bold flex items-center justify-center bg-gradient-to-br from-orange-500 to-yellow-400 hover:scale-105 hover:brightness-110 transition duration-150 shadow-md"
            onClick={() =>
              reviewMutation.mutate({ flashcardId: card.id, quality: q })
            }
          >
            {q}
          </button>
        ))}
      </div>

      {/* Toggle Button */}
      <div className="flex justify-center">
        <button
          className={`px-5 py-2 rounded-full text-sm font-medium transition shadow-md
      ${
        showAnswer
          ? "bg-indigo-500 hover:bg-indigo-600 text-white"
          : "bg-indigo-500 hover:bg-indigo-600 text-white"
      }
      disabled:bg-indigo-300 disabled:text-white/80 disabled:cursor-not-allowed
      focus:outline-none focus:ring-2 focus:ring-white/40`}
          onClick={() => setShowAnswer((v) => !v)}
        >
          {showAnswer ? "Show Question" : "Show Answer"}
        </button>
      </div>
    </div>
  );
}
