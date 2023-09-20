class PostalCodeBatcher:
    def __init__(self, postal_codes, batch_size):
        self.postal_codes = postal_codes
        self.batch_size = batch_size
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.postal_codes):
            self.current_index = 0

        start = self.current_index
        end = min(start + self.batch_size, len(self.postal_codes))

        self.current_index = end

        return self.postal_codes[start:end]

    def get_next_batch(self):
        return next(self)
