import re

class CompactList(list):
    pattern = re.compile(r'^$')               # Override this in subclasses

    @classmethod
    def _reduceList(cls, seq):
        l = sorted(set(seq), key=int)
        low, high = l[0], l[0]
        for v in l[1:]:
            if int(v) == int(high) + 1:       # Extend range
                high = v

            # There's a gap in the numbers
            elif int(high) - int(low) == 1:   # Two consecutive numbers
                yield low, low
                yield high, high
                low = high = v
            else:                             # Range
                yield low, high
                low = high = v

        # Final range
        if int(high) - int(low) == 1:         # Two consecutive numbers
            yield low, low
            yield high, high

        else:                                 # Range
            yield low, high

    @classmethod
    def _formatElement(cls, low, high):
        if low == high:
            return low
        else:
            return "%s-%s" % (low, high)

    @classmethod
    def _formatList(cls, seq):
        return ','.join(cls._formatElement(*e) for e in seq)

    def _getNumber(self, m):
        raise NotImplemented()

    def _getGeneric(self, m):
        raise NotImplemented()

    def __compactList(self):
        sequences = {}
        results = set()

        for i in self.__iter__():
            try:
                m = self.pattern.search(i).groupdict()
                try:
                    sequences[self._getGeneric(m)].append(self._getNumber(m))
                except KeyError:
                    sequences[self._getGeneric(m)] = [self._getNumber(m)]
            except AttributeError:
                # Regex didn't match. Print it unchanged.
                results.add(i)

        # Format the sequences. Sequences with only one entry should be a
        # regular-looking file name. Other sequences have brackets...
        for s, nums in sequences.items():
            nums = list(set(nums))
            if len(nums) > 1:
                results.add(s.format('[' + self._formatList(self._reduceList(nums)) + ']'))
            elif nums[0]:
                results.add(s.format(nums[0]))
            else:
                results.add(s.format(''))
        return results

    def __getslice__(self, i, j):
        return self.__class__(list.__getslice__(self, i, j))

    def itercompact(self):
        compactList = self.__compactList()
        for i in compactList:
            yield i
