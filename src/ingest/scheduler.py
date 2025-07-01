from datetime import datetime, timedelta

class SM2Scheduler:
    """
    Implements the SM-2 spaced repetition algorithm.
    Each flashcard review returns an ease rating (1–5), and the scheduler computes
    the next review date along with updating the repetition count and interval.
    """
    def __init__(self, ease: float = 2.5, interval: int = 1, repetitions: int = 0):
        # EF (easiness factor), I (interval in days), n (repetition count)
        self.easiness = ease
        self.interval = interval
        self.repetitions = repetitions

    def review(self, quality: int, review_date: datetime = None):
        """
        Process a review with quality rating (0-5).
        Returns: (next_due: datetime, new_EF: float, new_interval: int, new_repetitions: int)
        """
        if review_date is None:
            review_date = datetime.utcnow()

        # Ensure quality in [0,5]
        q = max(0, min(5, quality))

        # Update EF
        ef = self.easiness + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        if ef < 1.3:
            ef = 1.3

        # Determine interval
        if q < 3:
            # reset repetitions on failure
            n = 0
            i = 1
        else:
            n = self.repetitions + 1
            if n == 1:
                i = 1
            elif n == 2:
                i = 6
            else:
                i = round(self.interval * ef)

        next_due = review_date + timedelta(days=i)
        # Update state
        self.easiness = ef
        self.interval = i
        self.repetitions = n

        return next_due, ef, i, n


# Example usage:
if __name__ == '__main__':
    sched = SM2Scheduler()
    # Simulate quality ratings for successive reviews
    for qual in [5, 5, 4, 3, 5]:
        due, ef, interval, reps = sched.review(qual)
        print(f"Q={qual} → next in {interval}d at {due.date()}, EF={ef:.2f}, reps={reps}")
