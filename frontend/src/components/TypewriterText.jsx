import React, { useEffect, useState } from 'react';

export default function TypewriterText({ text, speed = 120, pause = 1500 }) {
  const [displayed, setDisplayed] = useState('');
  const [index, setIndex] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => {
      if (!deleting) {
        if (index < text.length) {
          setDisplayed((prev) => prev + text[index]);
          setIndex(index + 1);
        } else {
          setDeleting(true);
        }
      } else {
        if (index > 0) {
          setDisplayed((prev) => prev.slice(0, -1));
          setIndex(index - 1);
        } else {
          setDeleting(false);
        }
      }
    }, deleting ? speed / 2 : speed);

    return () => clearTimeout(timeout);
  }, [index, deleting]);

  useEffect(() => {
    if (index === text.length && !deleting) {
      const pauseTimer = setTimeout(() => setDeleting(true), pause);
      return () => clearTimeout(pauseTimer);
    }
  }, [index, deleting, pause, text.length]);

  return (
    <span className="inline-block font-medium text-white/80">
      {displayed}
      <span className="blinking-cursor">|</span>
    </span>
  );
}
