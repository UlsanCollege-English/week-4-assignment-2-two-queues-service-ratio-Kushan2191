from collections import deque

class Gate:
    def __init__(self):
        # Pattern is 1 fastpass, then 3 regulars
        self._pattern = ["fastpass", "regular", "regular", "regular"]
        self._idx = 0
        self._fast = deque()
        self._reg = deque()

    def arrive(self, line, person_id):
        """Add a person to the selected line."""
        if line == "fastpass":
            self._fast.append(person_id)
        elif line == "regular":
            self._reg.append(person_id)
        else:
            raise ValueError("Unknown line type")

    def _try_serve(self, queue):
        """Helper to serve from a queue if possible."""
        if queue:
            person = queue.popleft()
            self._idx = (self._idx + 1) % len(self._pattern)
            return person
        return None

    def serve(self):
        """
        Serve the next person according to the repeating pattern.
        Skips empty lines but still advances the cycle pointer.
        Raises IndexError if both queues are empty.
        """
        if not self._fast and not self._reg:
            raise IndexError("Both lines are empty")

        while True:
            line_to_serve = self._pattern[self._idx]
            if line_to_serve == "fastpass":
                person = self._try_serve(self._fast)
                if person is not None:
                    return person
            elif line_to_serve == "regular":
                person = self._try_serve(self._reg)
                if person is not None:
                    return person

            # If chosen queue was empty → advance pointer and try again
            self._idx = (self._idx + 1) % len(self._pattern)

    def peek_next_line(self):
        """
        Predict which line will serve next without dequeuing anyone.
        Returns "fastpass", "regular", or None if all queues are empty.
        """
        if not self._fast and not self._reg:
            return None

        temp_idx = self._idx
        checked_slots = 0
        pattern_len = len(self._pattern)

        # At most one full cycle is needed
        while checked_slots < pattern_len:
            line = self._pattern[temp_idx]
            if line == "fastpass" and self._fast:
                return "fastpass"
            if line == "regular" and self._reg:
                return "regular"

            temp_idx = (temp_idx + 1) % pattern_len
            checked_slots += 1

        return None  # queues empty or unreachable
